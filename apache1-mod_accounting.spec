%define		mod_name	accounting
%define 	apxs		%{_sbindir}/apxs
Summary:	Apache module: record traffic statistics into a database
Summary(pl):	Modu³ do apache: zapisuje statystyki ruchu do bazy danych
Name:		apache-mod_%{mod_name}
Version:	0.4
Release:	5
License:	BSD
Group:		Networking/Daemons
Source0:	http://prdownloads.sourceforge.net/mod-acct/mod_accounting-%{version}.tar.gz
# Source0-md5:	93076acba346fb37834ada9d9f630fa4
Source1:	%{name}.conf
URL:		http://sourceforge.net/projects/mod-acct/
BuildRequires:	apache(EAPI)-devel
BuildRequires:	mysql-devel
BuildRequires:	postgresql-devel
Prereq:		%{_sbindir}/apxs
Requires:	apache(EAPI)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR)
%define		_sysconfdir	/etc/httpd

%description
mod_accounting is a simple Apache module that can record traffic
statistics into a database (bytes in/out per http request)

%description -l pl
mod_accounting to prosty modu³ Apache pozwalaj±cy na zapisywanie
informacji o ruchu http do bazy danych (bajty
przychodz±ce/wychodz±ce).

%prep
%setup -q -n mod_%{mod_name}-%{version}

%build
PATH=$PATH:%{_sbindir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{_sysconfdir}}

install mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/mod_accounting.conf

%post
%{apxs} -e -a -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
if [ -f /etc/httpd/httpd.conf ] && ! grep -q "^Include.*mod_accounting.conf" /etc/httpd/httpd.conf; then
	echo "Include /etc/httpd/mod_accounting.conf" >> /etc/httpd/httpd.conf
fi
if [ -f /var/lock/subsys/httpd ]; then
	/etc/rc.d/init.d/httpd restart 1>&2
fi

%preun
if [ "$1" = "0" ]; then
	%{apxs} -e -A -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
	grep -v "^Include.*mod_accounting.conf" /etc/httpd/httpd.conf > \
		/etc/httpd/httpd.conf.tmp
	mv -f /etc/httpd/httpd.conf.tmp /etc/httpd/httpd.conf
	if [ -f /var/lock/subsys/httpd ]; then
		/etc/rc.d/init.d/httpd restart 1>&2
	fi
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README ChangeLog
%attr(755,root,root) %{_pkglibdir}/*

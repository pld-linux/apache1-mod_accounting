%define		mod_name	accounting
%define 	apxs		%{_sbindir}/apxs1
Summary:	Apache module: record traffic statistics into a database
Summary(pl):	Modu� do apache: zapisuje statystyki ruchu do bazy danych
Name:		apache1-mod_%{mod_name}
Version:	0.5
Release:	0.1
License:	BSD
Group:		Networking/Daemons
Source0:	http://dl.sourceforge.net/mod-acct/mod_accounting-%{version}.tar.gz
# Source0-md5:	fc045bbdc5ae32241765fea2967a63fb
Source1:	%{name}.conf
URL:		http://sourceforge.net/projects/mod-acct/
BuildRequires:	apache1-devel
BuildRequires:	mysql-devel
BuildRequires:	postgresql-devel
Requires(post,preun):	%{apxs}
Requires(post,preun):	grep
Requires(preun):	fileutils
Requires:	apache1
Obsoletes:	apache-mod_%{mod_name} <= %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR)
%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR)

%description
mod_accounting is a simple Apache module that can record traffic
statistics into a database (bytes in/out per HTTP request)

%description -l pl
mod_accounting to prosty modu� Apache pozwalaj�cy na zapisywanie
informacji o ruchu HTTP do bazy danych (bajty
przychodz�ce/wychodz�ce).

%prep
%setup -q -n mod_%{mod_name}-%{version}

%build
PATH=$PATH:%{_sbindir}
%{__make} \
	APXS=%{apxs} \
	LIB="%{_includedir}/postgresql %{_includedir}/mysql -lpq -lmysqlclient"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{_sysconfdir}}

install mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/mod_accounting.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{apxs} -e -a -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
if [ -f /etc/apache/apache.conf ] && ! grep -q "^Include.*mod_accounting.conf" /etc/apache/apache.conf; then
        echo "Include /etc/apache/mod_accounting.conf" >> /etc/apache/apache.conf
fi
if [ -f /var/lock/subsys/apache ]; then
	/etc/rc.d/init.d/apache restart 1>&2
fi

%preun
if [ "$1" = "0" ]; then
	%{apxs} -e -A -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
	umask 027
        grep -v "^Include.*mod_accounting.conf" /etc/apache/apache.conf > \
                /etc/apache/apache.conf.tmp
        mv -f /etc/apache/apache.conf.tmp /etc/apache/apache.conf
	if [ -f /var/lock/subsys/apache ]; then
		/etc/rc.d/init.d/apache restart 1>&2
	fi
fi

%files
%defattr(644,root,root,755)
%doc README ChangeLog
%attr(755,root,root) %{_pkglibdir}/*

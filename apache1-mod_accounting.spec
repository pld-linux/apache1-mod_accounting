# TODO
# - ipv6 patch not implemented
%bcond_without	ipv6		# disable IPv6 support

%define		mod_name	accounting
%define 	apxs		%{_sbindir}/apxs1
Summary:	Apache module: record traffic statistics into a database
Summary(pl):	Modu³ do apache: zapisuje statystyki ruchu do bazy danych
Name:		apache1-mod_%{mod_name}
Version:	0.5
Release:	0.5
License:	BSD
Group:		Networking/Daemons
Source0:	http://dl.sourceforge.net/mod-acct/mod_accounting-%{version}.tar.gz
# Source0-md5:	fc045bbdc5ae32241765fea2967a63fb
Source1:	%{name}.conf
URL:		http://sourceforge.net/projects/mod-acct/
BuildRequires:	apache1-devel >= 1.3.33-2
BuildRequires:	mysql-devel
BuildRequires:	postgresql-devel
%{?with_ipv6:BuildRequires:	apache1(ipv6)-devel}
%{!?with_ipv6:BuildConflicts:	apache1(ipv6)-devel}
Requires:	apache1 >= 1.3.33-2
Obsoletes:	apache-mod_%{mod_name} <= %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR 2>/dev/null)
%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)

%description
mod_accounting is a simple Apache module that can record traffic
statistics into a database (bytes in/out per HTTP request)

%description -l pl
mod_accounting to prosty modu³ Apache pozwalaj±cy na zapisywanie
informacji o ruchu HTTP do bazy danych (bajty
przychodz±ce/wychodz±ce).

%prep
%setup -q -n mod_%{mod_name}-%{version}

%build
PATH=$PATH:%{_sbindir}
%{__make} \
	APXS=%{apxs} \
	LIB="-L%{_includedir}/postgresql -L%{_includedir}/mysql -lpq -lmysqlclient"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{_sysconfdir}/conf.d}

install mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/90_mod_%{mod_name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f /var/lock/subsys/apache ]; then
	/etc/rc.d/init.d/apache restart 1>&2
fi

%postun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/apache ]; then
		/etc/rc.d/init.d/apache restart 1>&2
	fi
fi

%files
%defattr(644,root,root,755)
%doc README ChangeLog
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/conf.d/*_mod_%{mod_name}.conf
%attr(755,root,root) %{_pkglibdir}/*

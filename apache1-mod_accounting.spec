# TODO
# - ipv6 patch not implemented
%bcond_without	ipv6		# disable IPv6 support

%define		mod_name	accounting
%define 	apxs		%{_sbindir}/apxs1
Summary:	Apache module: record traffic statistics into a database
Summary(pl.UTF-8):	Moduł do apache: zapisuje statystyki ruchu do bazy danych
Name:		apache1-mod_%{mod_name}
Version:	0.5
Release:	0.6
License:	BSD
Group:		Networking/Daemons
Source0:	http://dl.sourceforge.net/mod-acct/mod_accounting-%{version}.tar.gz
# Source0-md5:	fc045bbdc5ae32241765fea2967a63fb
Source1:	%{name}.conf
URL:		http://sourceforge.net/projects/mod-acct/
%{?with_ipv6:BuildRequires:	apache1(ipv6)-devel}
BuildRequires:	apache1-devel >= 1.3.39
BuildRequires:	mysql-devel
BuildRequires:	postgresql-devel
BuildRequires:	rpmbuild(macros) >= 1.268
%{!?with_ipv6:BuildConflicts:	apache1(ipv6)-devel}
Requires:	apache1(EAPI)
Obsoletes:	apache-mod_accounting <= 0.5
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR 2>/dev/null)
%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)/conf.d

%description
mod_accounting is a simple Apache module that can record traffic
statistics into a database (bytes in/out per HTTP request)

%description -l pl.UTF-8
mod_accounting to prosty moduł Apache pozwalający na zapisywanie
informacji o ruchu HTTP do bazy danych (bajty
przychodzące/wychodzące).

%prep
%setup -q -n mod_%{mod_name}-%{version}

%build
PATH=$PATH:%{_sbindir}
%{__make} \
	APXS=%{apxs} \
	LIB="-L%{_includedir}/postgresql -L%{_includedir}/mysql -lpq -lmysqlclient"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{_sysconfdir}}

install mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/90_mod_%{mod_name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%service -q apache restart

%postun
if [ "$1" = "0" ]; then
	%service -q apache restart
fi

%files
%defattr(644,root,root,755)
%doc README ChangeLog
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*_mod_%{mod_name}.conf
%attr(755,root,root) %{_pkglibdir}/*

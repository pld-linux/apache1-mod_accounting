%define		mod_name	accounting
%define 	apxs		/usr/sbin/apxs
Summary:	Apache module: records traffic statistics into a database 
Summary(pl):	Modu³ do apache: zapisuje statystyki ruchu do relacyjnej bazy danych
Name:		apache-mod_%{mod_name}
Version:	0.4
Release:	1
License:	GPL
Group:		Networking/Daemons
Group(cs):	Sí»ové/Démoni
Group(da):	Netværks/Dæmoner
Group(de):	Netzwerkwesen/Server
Group(es):	Red/Servidores
Group(fr):	Réseau/Serveurs
Group(is):	Net/Púkar
Group(it):	Rete/Demoni
Group(no):	Nettverks/Daemoner
Group(pl):	Sieciowe/Serwery
Group(pt):	Rede/Servidores
Group(ru):	óÅÔØ/äÅÍÏÎÙ
Group(sl):	Omre¾ni/Stre¾niki
Group(sv):	Nätverk/Demoner
Group(uk):	íÅÒÅÖÁ/äÅÍÏÎÉ
Source0:	http://prdownloads.sourceforge.net/mod-acct/mod_%{mod_name}-%{version}.tar.gz
URL:		http://sourceforge.net/projects/mod-acct/
BuildRequires:	%{apxs}
BuildRequires:	apache-devel
BuildRequires:	zlib-devel
Prereq:		%{_sbindir}/apxs
Requires:	apache
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR)

%description
mod_accounting is a simple Apache module that can record traffic statistics
into a database (bytes in/out per http request).

%description -l pl
mod_accounting jest prostym modu³em Apacza, s³u¿±cym do zapisywania statystyk
ruchu do relacyjnej bazy danych (ilo¶æ bajtów wchodz±cych/wychodz±cych na
¿adanie http)

%prep 
%setup -q -n mod_%{mod_name}-%{version}

%build
%{apxs} -c mod_%{mod_name}.c -o mod_%{mod_name}.so -lz

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_pkglibdir}

install mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{_sbindir}/apxs -e -a -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
if [ -f /var/lock/subsys/httpd ]; then
	/etc/rc.d/init.d/httpd restart 1>&2
fi

%preun
if [ "$1" = "0" ]; then
	%{_sbindir}/apxs -e -A -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
	if [ -f /var/lock/subsys/httpd ]; then
		/etc/rc.d/init.d/httpd restart 1>&2
	fi
fi

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_pkglibdir}/*

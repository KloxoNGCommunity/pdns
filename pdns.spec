%global _hardened_build 1
%global backends %{nil}

Summary:		PowerDNS is a Versatile Database Driven Nameserver
Name:			pdns
Version:		4.8.4
Release:		2.kng%{dist}
Epoch:			0
License:		GPLv2
Group:			System Environment/Daemons
URL:			http://powerdns.com/
Source0:		http://downloads.powerdns.com/releases/%{name}-%{version}.tar.bz2
ExcludeArch: %{arm} %{ix86}

Requires(pre): shadow-utils
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

BuildRequires: make

BuildRequires: bison
BuildRequires: boost-devel
BuildRequires: gcc-c++
BuildRequires:		krb5-devel
BuildRequires: libcurl-devel
BuildRequires:  	libsodium-devel
%if 0%{?rhel} == 9
BuildRequires: 		lua-devel
%define lua_implementation lua
%else
%ifarch aarch64 ppc64le s390x
%define lua_implementation lua
BuildRequires: lua-devel
%else
BuildRequires: 		luajit-devel
%define lua_implementation luajit
%endif
%endif
BuildRequires: openssl-devel
BuildRequires: p11-kit-devel
BuildRequires: perl
BuildRequires: protobuf-compiler
BuildRequires: protobuf-devel
BuildRequires: libcurl-devel
BuildRequires: systemd

Provides: powerdns = %{version}-%{release}
%global backends %{backends} bind

Obsoletes: pdns-backend-geoip < 4.1.11-3
Obsoletes: pdns-backend-lua < 4.2.0-3
Obsoletes: pdns-backend-mydns < 4.2.0-3

%description
The PowerDNS Nameserver is a modern, advanced and high performance
authoritative-only nameserver. It is written from scratch and conforms
to all relevant DNS standards documents.
Furthermore, PowerDNS interfaces with almost any database.

%package tools
Summary: Extra tools for %{name}

%description tools
This package contains the extra tools for %{name}

%package backend-mysql
Summary: MySQL backend for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
BuildRequires: mariadb-connector-c-devel openssl-devel
%global backends %{backends} gmysql

%description backend-mysql
This package contains the gmysql backend for %{name}

%package backend-postgresql
Summary: PostgreSQL backend for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
BuildRequires: libpq-devel
%global backends %{backends} gpgsql

%description backend-postgresql
This package contains the gpgsql backend for %{name}

%package backend-pipe
Summary: Pipe backend for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
%global backends %{backends} pipe

%description backend-pipe
This package contains the pipe backend for %{name}

%package backend-remote
Summary: Remote backend for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
%global backends %{backends} remote

%description backend-remote
This package contains the remote backend for %{name}

%package backend-ldap
Summary: LDAP backend for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
BuildRequires: openldap-devel
%global backends %{backends} ldap

%description backend-ldap
This package contains the ldap backend for %{name}

%package backend-lua2
Summary: LUA2 backend for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
%global backends %{backends} lua2

%description backend-lua2
This package contains the lua2 backend for %{name}

%package backend-sqlite
Summary: SQLite backend for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
BuildRequires: sqlite-devel
%global backends %{backends} gsqlite3

%description backend-sqlite
This package contains the SQLite backend for %{name}

%package backend-geoip
Summary: Geo backend for %{name}
Group: System Environment/Daemons
Requires: %{name}%{?_isa} = %{version}-%{release}
BuildRequires: yaml-cpp-devel

BuildRequires: libmaxminddb-devel
%global backends %{backends} geoip

%description backend-geoip
This package contains the geoip backend for %{name}
It allows different answers to DNS queries coming from different
IP address ranges or based on the geoipgraphic location


%package backend-tinydns
Summary: TinyDNS backend for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
BuildRequires: tinycdb-devel
%global backends %{backends} tinydns

%description backend-tinydns
This package contains the TinyDNS backend for %{name}

%package ixfrdist
Summary: A program to redistribute zones over AXFR and IXFR
BuildRequires: yaml-cpp-devel

%description ixfrdist
This package contains the ixfrdist program.

%prep
%autosetup -p1

%build
export CPPFLAGS="-DLDAP_DEPRECATED"

%configure \
    --enable-option-checking=fatal \
    --sysconfdir=%{_sysconfdir}/%{name} \
    --disable-static \
	--disable-dependency-tracking \
    --disable-silent-rules \
	--with-modules='' \
	--with-lua=%{lua_implementation} \
	--with-dynmodules='%{backends}' \
    --enable-tools \
    --with-libsodium \
   --enable-ixfrdist \
    --enable-unit-tests \
   --enable-lua-records \
   --enable-experimental-pkcs11 \
	--enable-dns-over-tls \
	--enable-systemd

%make_build

%install
%make_install
%{__rm} -f %{buildroot}%{_libdir}/%{name}/*.la
%{__mv} %{buildroot}%{_sysconfdir}/%{name}/pdns.conf{-dist,}

# rename zone2ldap to pdns-zone2ldap (#1193116)
%{__mv} %{buildroot}/%{_bindir}/zone2ldap %{buildroot}/%{_bindir}/pdns_zone2ldap
%{__mv} %{buildroot}/%{_mandir}/man1/zone2ldap.1 %{buildroot}/%{_mandir}/man1/pdns_zone2ldap.1

# change user/group to pdns
# change default backend to bind
sed -i \
    -e 's/# setuid=/setuid=pdns/' \
    -e 's/# setgid=/setgid=pdns/' \
    -e 's/# launch=/launch=bind/' \
    -e 's/# security-poll-suffix=secpoll\.powerdns\.com\./security-poll-suffix=/' \
    %{buildroot}%{_sysconfdir}/%{name}/pdns.conf

%{__rm} %{buildroot}/%{_bindir}/stubquery
%{__install } -d %{buildroot}/%{_sharedstatedir}/%{name}

%check
make %{?_smp_mflags} -C pdns check

%pre

getent group pdns >/dev/null || groupadd -r pdns
getent passwd pdns >/dev/null || \
	useradd -r -g pdns -d /var/lib/pdns -s /sbin/nologin \
	-c "PowerDNS Authoritative Server" pdns
# Change home directory to /var/lib/pdns
if [[ $(getent passwd pdns | cut -d: -f6) == "/" ]]; then
    usermod -d /var/lib/pdns pdns
fi
exit 0

%post
%systemd_post pdns.service


%preun
%systemd_preun pdns.service

%postun
%systemd_postun_with_restart pdns.service


%files
%doc README
%license COPYING
%{_bindir}/pdns_control
%{_bindir}/pdnsutil
%{_bindir}/pdns_zone2ldap
%{_bindir}/zone2sql
%{_bindir}/zone2json
%{_sbindir}/pdns_server
%{_mandir}/man1/pdns_control.1.gz
%{_mandir}/man1/pdns_server.1.gz
%{_mandir}/man1/zone2sql.1.gz
%{_mandir}/man1/zone2json.1.gz
%{_mandir}/man1/pdns_zone2ldap.1.gz
%{_mandir}/man1/pdnsutil.1.gz
%{_unitdir}/pdns.service
%{_unitdir}/pdns@.service
%{_libdir}/%{name}/libbindbackend.so
%dir %{_libdir}/%{name}/
%dir %attr(-,pdns,pdns) %{_sharedstatedir}/%{name}
%dir %attr(-,root,pdns) %{_sysconfdir}/%{name}/
%attr(0640,root,pdns) %config(noreplace) %{_sysconfdir}/%{name}/pdns.conf

%files tools
 %{_bindir}/calidns
 %{_bindir}/dnsbulktest
 %{_bindir}/dnsgram
%{_bindir}/dnspcap2calidns
%{_bindir}/dnspcap2protobuf
 %{_bindir}/dnsreplay
 %{_bindir}/dnsscan
 %{_bindir}/dnsscope
 %{_bindir}/dnstcpbench
 %{_bindir}/dnswasher
 %{_bindir}/dumresp
 %{_bindir}/ixplore
%{_bindir}/pdns_notify
 %{_bindir}/nproxy
 %{_bindir}/nsec3dig
 %{_bindir}/saxfr
 %{_bindir}/sdig
 %{_mandir}/man1/calidns.1.gz
 %{_mandir}/man1/dnsbulktest.1.gz
 %{_mandir}/man1/dnsgram.1.gz
%{_mandir}/man1/dnspcap2calidns.1.gz
%{_mandir}/man1/dnspcap2protobuf.1.gz
 %{_mandir}/man1/dnsreplay.1.gz
 %{_mandir}/man1/dnsscan.1.gz
 %{_mandir}/man1/dnsscope.1.gz
 %{_mandir}/man1/dnstcpbench.1.gz
 %{_mandir}/man1/dnswasher.1.gz
 %{_mandir}/man1/dumresp.1.gz
 %{_mandir}/man1/ixplore.1.gz
%{_mandir}/man1/pdns_notify.1.gz
 %{_mandir}/man1/nproxy.1.gz
 %{_mandir}/man1/nsec3dig.1.gz
 %{_mandir}/man1/saxfr.1.gz
 %{_mandir}/man1/sdig.1.gz
%{_pkgdocdir}/bind-dnssec.4.2.0_to_4.3.0_schema.sqlite3.sql
%{_pkgdocdir}/bind-dnssec.schema.sqlite3.sql

%files backend-mysql
%{_pkgdocdir}/schema.mysql.sql
%{_pkgdocdir}/dnssec-3.x_to_3.4.0_schema.mysql.sql
%{_pkgdocdir}/nodnssec-3.x_to_3.4.0_schema.mysql.sql
%{_pkgdocdir}/3.4.0_to_4.1.0_schema.mysql.sql
%{_pkgdocdir}/4.1.0_to_4.2.0_schema.mysql.sql
%{_pkgdocdir}/4.2.0_to_4.3.0_schema.mysql.sql
%{_pkgdocdir}/4.3.0_to_4.7.0_schema.mysql.sql
%{_pkgdocdir}/enable-foreign-keys.mysql.sql
%{_libdir}/%{name}/libgmysqlbackend.so 


%files backend-postgresql
%{_pkgdocdir}/schema.pgsql.sql
%{_pkgdocdir}/dnssec-3.x_to_3.4.0_schema.pgsql.sql
%{_pkgdocdir}/nodnssec-3.x_to_3.4.0_schema.pgsql.sql
%{_pkgdocdir}/3.4.0_to_4.1.0_schema.pgsql.sql
%{_pkgdocdir}/4.1.0_to_4.2.0_schema.pgsql.sql
%{_pkgdocdir}/4.2.0_to_4.3.0_schema.pgsql.sql
%{_pkgdocdir}/4.3.0_to_4.7.0_schema.pgsql.sql
%{_libdir}/%{name}/libgpgsqlbackend.so

%files backend-pipe
%{_libdir}/%{name}/libpipebackend.so

%files backend-remote
%{_libdir}/%{name}/libremotebackend.so

%files backend-ldap
%{_libdir}/%{name}/libldapbackend.so
%{_pkgdocdir}/dnsdomain2.schema
%{_pkgdocdir}/pdns-domaininfo.schema

%files backend-lua2
%{_libdir}/%{name}/liblua2backend.so


%files backend-sqlite
%{_pkgdocdir}/schema.sqlite3.sql
%{_pkgdocdir}/dnssec-3.x_to_3.4.0_schema.sqlite3.sql
%{_pkgdocdir}/nodnssec-3.x_to_3.4.0_schema.sqlite3.sql
%{_pkgdocdir}/3.4.0_to_4.0.0_schema.sqlite3.sql
%{_pkgdocdir}/4.0.0_to_4.2.0_schema.sqlite3.sql
%{_pkgdocdir}/4.2.0_to_4.3.0_schema.sqlite3.sql
%{_pkgdocdir}/4.3.0_to_4.3.1_schema.sqlite3.sql
%{_pkgdocdir}/4.3.1_to_4.7.0_schema.sqlite3.sql
%{_libdir}/%{name}/libgsqlite3backend.so

%files backend-tinydns
%{_libdir}/%{name}/libtinydnsbackend.so

%files ixfrdist
%{_bindir}/ixfrdist
%{_mandir}/man1/ixfrdist.1.gz
%{_mandir}/man5/ixfrdist.yml.5.gz
%{_sysconfdir}/%{name}/ixfrdist.example.yml
%{_unitdir}/ixfrdist.service
%{_unitdir}/ixfrdist@.service

%files backend-geoip
%{_libdir}/%{name}/libgeoipbackend.so



%changelog

* Mon Aug 26 2024 John Pierce <john@luckyanuki.com>  - 4.8.4-1.kng
- Conform to Fedora spec 4.8.4 but maintain geoip backend

* Sun Mar 22 2020 Dionysis Kladis <dkstiler@gmail.com> 4.2.1-1.kng
- Update to version 4.2.1 
- Added new features support with newer source
- Fixed errors for documents and missing files
- Get in sync with the spec file from the source repository https://github.com/PowerDNS/pdns/blob/master/builder-support/specs/pdns.spec

* Mon Dec 23 2019 John Pierce <john@luckytanuki.com> 4.1.13-2
- Build for Kloxo NG

* Thu Aug 08 2019 Kees Monshouwer <mind04@monshouwer.org> 4.1.13-1
- update to version 4.1.13

* Wed Aug 07 2019 Kees Monshouwer <mind04@monshouwer.org> 4.1.12-1
- update to version 4.1.12

* Tue Jul 30 2019 Kees Monshouwer <mind04@monshouwer.org> 4.1.11-1
- update to version 4.1.11

* Thu Jun 20 2019 Kees Monshouwer <mind04@monshouwer.org> 4.1.10-1
- update to version 4.1.10

* Tue Jun 18 2019 Kees Monshouwer <mind04@monshouwer.org> 4.1.9-1
- update to version 4.1.9

* Fri Mar 22 2019 Kees Monshouwer <mind04@monshouwer.org> 4.1.8-1
- update to version 4.1.8

* Mon Mar 18 2019 Kees Monshouwer <mind04@monshouwer.org> 4.1.7-1
- update to version 4.1.7

* Wed Jan 30 2019 Kees Monshouwer <mind04@monshouwer.org> 4.1.6-1
- update to version 4.1.6

* Tue Nov 06 2018 Kees Monshouwer <mind04@monshouwer.org> 4.1.5-1
- update to version 4.1.5

* Wed Aug 29 2018 Kees Monshouwer <mind04@monshouwer.org> 4.1.4-1
- update to version 4.1.4

* Thu May 24 2018 Kees Monshouwer <mind04@monshouwer.org> 4.1.3-1
- update to version 4.1.3

* Mon May 07 2018 Kees Monshouwer <mind04@monshouwer.org> 4.1.2-1
- update to version 4.1.2

* Fri Feb 16 2018 Kees Monshouwer <mind04@monshouwer.org> 4.1.1-1
- update to version 4.1.1

* Thu Nov 30 2017 Kees Monshouwer <mind04@monshouwer.org> 4.1.0-1
- update to version 4.1.0

* Mon Nov 27 2017 Kees Monshouwer <mind04@monshouwer.org> 4.0.5-1
- update to version 4.0.5

* Thu Jun 22 2017 Kees Monshouwer <mind04@monshouwer.org> 4.0.4-1
- update to version 4.0.4

* Tue Jan 17 2017 Kees Monshouwer <mind04@monshouwer.org> 4.0.3-1
- update to version 4.0.3

* Fri Jan 13 2017 Kees Monshouwer <mind04@monshouwer.org> 4.0.2-1
- update to version 4.0.2

* Fri Jul 29 2016 Kees Monshouwer <mind04@monshouwer.org> 4.0.1-1
- update to version 4.0.1

* Mon Jul 11 2016 Kees Monshouwer <mind04@monshouwer.org> 4.0.0-1
- update to version 4.0.0
- add ixplore, sdig and dnspcap2protobuf to tools
- rename pdnssec to pdnsutil
- remove geo backend

* Thu Aug 27 2015 Kees Monshouwer <mind04@monshouwer.org> 3.4.6-1
- update to version 3.4.6

* Tue Jun 09 2015 Kees Monshouwer <mind04@monshouwer.org> 3.4.5-1
- update to version 3.4.5

* Thu Apr 23 2015 Kees Monshouwer <mind04@monshouwer.org> 3.4.4-1
- update to version 3.4.4

* Mon Mar 02 2015 Kees Monshouwer <mind04@monshouwer.org> 3.4.3-1
- update to version 3.4.3

* Tue Feb 03 2015 Kees Monshouwer <mind04@monshouwer.org> 3.4.2-1
- update to version 3.4.2
- move all manpages to section 1
- markdown based documentation

* Thu Oct 30 2014 Kees Monshouwer <mind04@monshouwer.org> 3.4.1-1
- update to 3.4.1
- disable security status polling by default https://github.com/PowerDNS/pdns/blob/master/pdns/docs/security-poll.md

* Sat Oct 11 2014 Kees Monshouwer <mind04@monshouwer.org> 3.4.0-2
- reorder spec file
- rename backend-sqlite3 to backend-sqlite
- add lua backend

* Tue Sep 30 2014 Kees Monshouwer <mind04@monshouwer.org> 3.4.0-1
- initial el7 build for PowerDNS server

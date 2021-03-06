#
# PowerDNS server el7 spec file
#
%global _hardened_build 1
%global backends %{nil}

Summary:		PowerDNS is a Versatile Database Driven Nameserver
Name:			pdns
Version:		4.2.1
Release:		1.kng%{dist}
Epoch:			0
License:		GPLv2
Group:			System Environment/Daemons
URL:			http://www.powerdns.com/
Source0:		http://downloads.powerdns.com/releases/pdns-%{version}.tar.bz2
Source1:		pdns.service

Patch0:			pdns-4.1.1-disable-secpoll.patch

Patch10:		pdns-git-init.patch


%if 0%{?rhel} == 6
BuildRequires:		devtoolset-7
BuildRequires:		boost-program-options
%endif
%if %{?fedora}0 > 150 || %{?rhel}0 >60
BuildRequires:		systemd-units
BuildRequires:		systemd-devel
BuildRequires:		gcc
BuildRequires:		gcc-c++

%endif
%if 0%{?rhel} >= 7
Requires(post): systemd-sysv
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units
BuildRequires: systemd
BuildRequires: systemd-units
BuildRequires: systemd-devel

BuildRequires: protobuf-devel
BuildRequires: protobuf-compiler
BuildRequires: p11-kit-devel
BuildRequires: libcurl-devel
BuildRequires: boost-devel
%else
BuildRequires: boost148-devel
BuildRequires: boost148-program-options
%endif

BuildRequires:		protobuf-devel
BuildRequires:		krb5-devel
BuildRequires:		boost-devel
BuildRequires:		sqlite-devel
BuildRequires:		openssl-devel
BuildRequires:		sqlite-devel

BuildRequires:  	autoconf
BuildRequires:  	automake
BuildRequires:  	bison
BuildRequires:  	curl-devel
BuildRequires:  	flex
BuildRequires:  	gdbm-devel
BuildRequires:  	libsodium-devel
BuildRequires:  	libtool
BuildRequires:  	pkgconfig
BuildRequires: 		lua-devel
BuildRequires: 		luajit-devel





Requires(pre):		shadow-utils
%if %{?fedora}0 > 150 || %{?rhel}0 >60
Requires(post):		systemd-sysv
Requires(post):		systemd-units
Requires(preun):	systemd-units
Requires(postun):	systemd-units
%endif


Provides: powerdns = %{version}-%{release}


%description
The PowerDNS Nameserver is a modern, advanced and high performance
authoritative-only nameserver. It is written from scratch and conforms
to all relevant DNS standards documents.
Furthermore, PowerDNS interfaces with almost any database.

%package		backend-bind
Summary:		Bind backend for %{name}
Group:			System Environment/Daemons
Requires:		%{name}%{?_isa} = %{epoch}:%{version}-%{release}
%global backends %{backends} bind

%description		backend-bind
The BindBackend parses a Bind-style named.conf and extracts information about
zones from it. It makes no attempt to honour other configuration flags,
which you should configure (when available) using the PDNS native configuration.


%package tools
Summary: Extra tools for %{name}
Group: System Environment/Daemons

%description tools
This package contains the extra tools for %{name}

%package backend-mysql
Summary: MySQL backend for %{name}
Group: System Environment/Daemons
Requires: %{name}%{?_isa} = %{version}-%{release}
BuildRequires: mysql-devel
%global backends %{backends} gmysql

%description backend-mysql
This package contains the gmysql backend for %{name}

%package backend-postgresql
Summary: PostgreSQL backend for %{name}
Group: System Environment/Daemons
Requires: %{name}%{?_isa} = %{version}-%{release}
BuildRequires: postgresql-devel
%global backends %{backends} gpgsql

%description backend-postgresql
This package contains the gpgsql backend for %{name}

%package backend-pipe
Summary: Pipe backend for %{name}
Group: System Environment/Daemons
Requires: %{name}%{?_isa} = %{version}-%{release}
%global backends %{backends} pipe

%description backend-pipe
This package contains the pipe backend for %{name}

%package backend-remote
Summary: Remote backend for %{name}
Group: System Environment/Daemons
Requires: %{name}%{?_isa} = %{version}-%{release}
%global backends %{backends} remote

%description backend-remote
This package contains the remote backend for %{name}

%package backend-ldap
Summary: LDAP backend for %{name}
Group: System Environment/Daemons
Requires: %{name}%{?_isa} = %{version}-%{release}
BuildRequires: openldap-devel
%global backends %{backends} ldap

%description backend-ldap
This package contains the LDAP backend for %{name}

%package		backend-mydns
Summary:		MyDNS backend for %{name}
Group:			System Environment/Daemons
Requires:		%{name}%{?_isa} = %{epoch}:%{version}-%{release}
BuildRequires:		mysql-devel
%global backends %{backends} mydns

%description		backend-mydns
This package contains the MyDNS backend for the PowerDNS nameserver.

%package backend-lua2
Summary: Lua2 backend for %{name}
Group: System Environment/Daemons
Requires: %{name}%{?_isa} = %{version}-%{release}
BuildRequires: lua-devel
%global backends %{backends} lua2

%description backend-lua2
This package contains the lua2 backend for %{name}

%package backend-sqlite
Summary: SQLite backend for %{name}
Group: System Environment/Daemons
Requires: %{name}%{?_isa} = %{version}-%{release}
BuildRequires: sqlite-devel
%global backends %{backends} gsqlite3

%description backend-sqlite
This package contains the SQLite backend for %{name}

%if 0%{?rhel} >= 7
%package backend-odbc
Summary: UnixODBC backend for %{name}
Group: System Environment/Daemons
Requires: %{name}%{?_isa} = %{version}-%{release}
BuildRequires: unixODBC-devel
%global backends %{backends} godbc

%description backend-odbc
This package contains the godbc backend for %{name}

%package backend-geoip
Summary: Geo backend for %{name}
Group: System Environment/Daemons
Requires: %{name}%{?_isa} = %{version}-%{release}
BuildRequires: yaml-cpp-devel
%if 0%{?rhel} <= 7
BuildRequires: geoip-devel
%endif
BuildRequires: libmaxminddb-devel
%global backends %{backends} geoip

%description backend-geoip
This package contains the geoip backend for %{name}
It allows different answers to DNS queries coming from different
IP address ranges or based on the geoipgraphic location

%package backend-lmdb
Summary: LMDB backend for %{name}
Group: System Environment/Daemons
Requires: %{name}%{?_isa} = %{version}-%{release}
BuildRequires: lmdb-devel
%global backends %{backends} lmdb

%description backend-lmdb
This package contains the lmdb backend for %{name}

%package backend-tinydns
Summary: TinyDNS backend for %{name}
Group: System Environment/Daemons
Requires: %{name}%{?_isa} = %{version}-%{release}
BuildRequires: tinycdb-devel
%global backends %{backends} tinydns

%description backend-tinydns
This package contains the TinyDNS backend for %{name}

%package ixfrdist
BuildRequires: yaml-cpp-devel
Summary: A progrm to redistribute zones over AXFR and IXFR
Group: System Environment/Daemons

%description ixfrdist
This package contains the ixfrdist program.
%endif


%prep
%autosetup -p1 -n pdns-%{version}

%if 0%{?rhel} == 6
%patch10 -p1 -b .init
%endif
# we will need secpoll in the future
#%patch0 -p1 -b .disable-secpoll


%build
export CPPFLAGS="-DLDAP_DEPRECATED"

%configure \
    --sysconfdir=%{_sysconfdir}/%{name} \
    --enable-option-checking=fatal \
    --with-sqlite3 \
    --with-protobuf \
    --disable-static \
    --disable-silent-rules \
    --with-modules="" \
    --with-lua=luajit \
    --with-libsodium \
    --with-dynmodules='%{backends} random' \
    --enable-tools \
    --enable-unit-tests \
%if 0%{?rhel} >= 7
   --enable-experimental-pkcs11 \
   --enable-lua-records \
   --enable-ixfrdist \
   --enable-systemd 
   %else
   --disable-lua-records \
   --without-protobuf \
   --with-boost=/usr/include/boost148/ LDFLAGS=-L/usr/lib64/boost148 \
   CXXFLAGS=-std=gnu++11
%endif

%if %{?fedora}0 > 150 || %{?rhel}0 >60
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
%endif

%{__make} %{?_smp_mflags}

%install
%{__make} DESTDIR=%{buildroot} install
%{__rm} -f %{buildroot}%{_libdir}/%{name}/*.la

install -d %{buildroot}%{_sysconfdir}/%{name}/

# fix the config
%{__mv} %{buildroot}%{_sysconfdir}/%{name}/pdns.conf-dist %{buildroot}%{_sysconfdir}/%{name}/pdns.conf

cat >> %{buildroot}%{_sysconfdir}/%{name}/pdns.conf << EOF
setuid=pdns
setgid=pdns
EOF

chmod 600 %{buildroot}%{_sysconfdir}/%{name}/pdns.conf

%if %{?fedora}0 > 150 || %{?rhel}0 >60
# install our systemd service file
%{__rm} -f %{buildroot}%{_unitdir}/pdns.service
%{__rm} -f %{buildroot}%{_unitdir}/pdns@.service
install -p -D -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/pdns.service
%else
%if 0%{?rhel} == 6
# install sysv scripts
install -d %{buildroot}%{_initrddir}
install -m755 pdns/pdns.init %{buildroot}%{_initrddir}/pdns
%endif
%endif

%if 0%{?rhel} >= 7
# rename zone2ldap to pdns-zone2ldap (#1193116)
%{__mv} %{buildroot}/%{_bindir}/zone2ldap %{buildroot}/%{_bindir}/pdns-zone2ldap
%{__mv} %{buildroot}/%{_mandir}/man1/zone2ldap.1 %{buildroot}/%{_mandir}/man1/pdns-zone2ldap.1
%endif

%check
PDNS_TEST_NO_IPV6=1 make %{?_smp_mflags} -C pdns check || (cat pdns/test-suite.log && false)

%pre

getent group pdns >/dev/null || groupadd -r pdns
getent passwd pdns >/dev/null || \
	useradd -r -g pdns -d / -s /sbin/nologin \
	-c "PowerDNS authoritative server user" pdns
exit 0

%if 0%{?rhel} >= 7
if [ "`stat -c '%U:%G' %{_sysconfdir}/%{name}`" = "root:root" ]; then
  chown -R root:pdns /etc/powerdns
  # Make sure that pdns can read it; the default used to be 0600
  chmod g+r /etc/powerdns/pdns.conf
fi
chown -R pdns:pdns /var/lib/powerdns || :
%endif

%post
%if 0%{?rhel} >= 7
systemctl daemon-reload ||:
%systemd_post pdns.service
%else
/sbin/chkconfig --add pdns
%endif

%preun
%if 0%{?rhel} >= 7
%systemd_preun pdns.service
%else
if [ $1 -eq 0 ]; then
  /sbin/service pdns stop >/dev/null 2>&1 || :
  /sbin/chkconfig --del pdns
fi
%endif

%postun
%if 0%{?rhel} >= 7
%systemd_postun_with_restart pdns.service
%else
if [ $1 -ge 1 ]; then
  /sbin/service pdns condrestart >/dev/null 2>&1 || :
fi
%endif


%files
%doc COPYING INSTALL NOTICE README
%dir %{_sysconfdir}/%{name}/
%dir %{_libdir}/%{name}/
%config(noreplace) %attr(0600,root,root) %{_sysconfdir}/%{name}/pdns.conf
%{_unitdir}/pdns.service
%{_bindir}/pdns_control
%{_bindir}/pdnsutil
%{_sbindir}/pdns_server
%{_mandir}/man1/pdns_control.1.gz
%{_mandir}/man1/pdns_server.1.gz
%{_mandir}/man1/pdnsutil.1.gz
%{_libdir}/%{name}/librandombackend.so

%files backend-bind
%{_libdir}/%{name}/libbindbackend.so
%doc pdns/bind-dnssec.schema.sqlite3.sql

%files backend-mysql
%{_libdir}/%{name}/libgmysqlbackend.so
%doc %{_defaultdocdir}/%{name}/schema.mysql.sql
%doc %{_defaultdocdir}/%{name}/nodnssec-3.x_to_3.4.0_schema.mysql.sql
%doc %{_defaultdocdir}/%{name}/dnssec-3.x_to_3.4.0_schema.mysql.sql
%doc %{_defaultdocdir}/%{name}/3.4.0_to_4.1.0_schema.mysql.sql
%doc %{_defaultdocdir}/%{name}/4.1.0_to_4.2.0_schema.mysql.sql

%files backend-postgresql
%{_libdir}/%{name}/libgpgsqlbackend.so
%doc %{_defaultdocdir}/%{name}/schema.pgsql.sql
%doc %{_defaultdocdir}/%{name}/nodnssec-3.x_to_3.4.0_schema.pgsql.sql
%doc %{_defaultdocdir}/%{name}/dnssec-3.x_to_3.4.0_schema.pgsql.sql
%doc %{_defaultdocdir}/%{name}/3.4.0_to_4.1.0_schema.pgsql.sql
%doc %{_defaultdocdir}/%{name}/4.1.0_to_4.2.0_schema.pgsql.sql

%files backend-sqlite
%{_libdir}/%{name}/libgsqlite3backend.so
%doc %{_defaultdocdir}/%{name}/schema.sqlite3.sql
%doc %{_defaultdocdir}/%{name}/nodnssec-3.x_to_3.4.0_schema.sqlite3.sql
%doc %{_defaultdocdir}/%{name}/dnssec-3.x_to_3.4.0_schema.sqlite3.sql
%doc %{_defaultdocdir}/%{name}/3.4.0_to_4.0.0_schema.sqlite3.sql
%doc %{_defaultdocdir}/%{name}/4.0.0_to_4.2.0_schema.sqlite3.sql

%files backend-ldap
%{_libdir}/%{name}/libldapbackend.so
%doc %{_defaultdocdir}/%{name}/dnsdomain2.schema
%doc %{_defaultdocdir}/%{name}/pdns-domaininfo.schema

%files backend-lua2
%{_libdir}/%{name}/liblua2backend.so
%doc modules/luabackend/README

%files backend-mydns
%{_libdir}/%{name}/libmydnsbackend.so
%doc %{_defaultdocdir}/%{name}/schema.mydns.sql

%files backend-pipe
%{_libdir}/%{name}/libpipebackend.so

%files backend-remote
%{_libdir}/%{name}/libremotebackend.so

%files tools
%{_bindir}/zone2json
%{_bindir}/pdns-zone2ldap
%{_bindir}/zone2sql
 %{_bindir}/calidns
 %{_bindir}/dnsbulktest
 %{_bindir}/pdns_control
 %{_bindir}/dnsgram
 %{_bindir}/dnsreplay
 %{_bindir}/dnsscan
 %{_bindir}/dnsscope
 %{_bindir}/dnstcpbench
 %{_bindir}/dnswasher
 %{_bindir}/dumresp
 %{_bindir}/ixplore
 %{_bindir}/nproxy
 %{_bindir}/nsec3dig
 %{_bindir}/pdns_notify
 %{_bindir}/dnspcap2protobuf
 %{_bindir}/saxfr
 %{_bindir}/sdig
 %{_bindir}/stubquery
 %{_bindir}/dnspcap2calidns
%{_mandir}/man1/zone2json.1.gz
%{_mandir}/man1/pdns-zone2ldap.1.gz
%{_mandir}/man1/zone2sql.1.gz
 %{_mandir}/man1/calidns.1.gz
 %{_mandir}/man1/dnsbulktest.1.gz
 %{_mandir}/man1/dnsgram.1.gz
 %{_mandir}/man1/dnsreplay.1.gz
 %{_mandir}/man1/dnsscan.1.gz
 %{_mandir}/man1/dnsscope.1.gz
 %{_mandir}/man1/dnstcpbench.1.gz
 %{_mandir}/man1/dnswasher.1.gz
 %{_mandir}/man1/dumresp.1.gz
 %{_mandir}/man1/ixplore.1.gz
 %{_mandir}/man1/nproxy.1.gz
 %{_mandir}/man1/nsec3dig.1.gz
 %{_mandir}/man1/pdns_notify.1.gz
 %{_mandir}/man1/dnspcap2protobuf.1.gz
 %{_mandir}/man1/dnspcap2calidns.1.gz
 %{_mandir}/man1/saxfr.1.gz
 %{_mandir}/man1/sdig.1.gz
 
 %if 0%{?rhel} >= 7
%files backend-odbc
%doc %{_defaultdocdir}/%{name}/schema.mssql.sql
%doc %{_defaultdocdir}/%{name}/4.0.0_to_4.2.0_schema.mssql.sql
%{_libdir}/%{name}/libgodbcbackend.so

%files backend-geoip
%{_libdir}/%{name}/libgeoipbackend.so

%files backend-lmdb
%{_libdir}/%{name}/liblmdbbackend.so

%files backend-tinydns
%{_libdir}/%{name}/libtinydnsbackend.so

%files ixfrdist
%{_bindir}/ixfrdist
%{_mandir}/man1/ixfrdist.1.gz
%{_mandir}/man5/ixfrdist.yml.5.gz
%{_sysconfdir}/%{name}/ixfrdist.example.yml
%{_unitdir}/ixfrdist.service
%{_unitdir}/ixfrdist@.service
%endif


%changelog
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

### Header
Name:           util-linux
Version:        2.33
Release:        1
License:        GPLv2 and GPLv2+ and BSD with advertising and Public Domain
Summary:        A collection of basic system utilities
Url:            http://kernel.org/~kzak/util-linux/
Group:          System/Base

### Macros
%define no_cfsfdisk_archs sparc sparcv9 sparc64

BuildRequires:  libtool
BuildRequires:  gettext-devel
BuildRequires:  pam-devel

### Dependences
BuildRequires:  pkgconfig(ext2fs) >= 1.36
BuildRequires:  pkgconfig(ncurses)
BuildRequires:  pkgconfig(popt)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  libutempter-devel
BuildRequires:  bison

### Sources
Source0:        %{name}-%{version}.tar.xz
Source1:        util-linux-login.pamd
Source2:        util-linux-remote.pamd
Source3:        util-linux-chsh-chfn.pamd
Source4:        util-linux-60-raw.rules
Source11:       util-linux-su.pamd
Source12:       util-linux-su-l.pamd
Source14:       util-linux-runuser.pamd
Source15:       util-linux-runuser-l.pamd

### Obsoletes & Conflicts & Provides
# old versions of e2fsprogs contain fsck, uuidgen
Conflicts: e2fsprogs <= 1.42.2
# rename from util-linux-ng back to util-linux
Obsoletes: util-linux-ng <= 2.20.1
Provides: util-linux-ng = %{version}-%{release}
Conflicts: filesystem < 3

Requires:       /etc/pam.d/system-auth
Requires:       pam >= 0.66-4
Provides:       mount
Requires: libuuid = %{version}-%{release}
Requires: libblkid = %{version}-%{release}
Requires: libmount = %{version}-%{release}
Requires: libsmartcols = %{version}-%{release}
Requires: libfdisk = %{version}-%{release}
# Ensure that /var/log/lastlog has owner (setup)
Requires: setup
Requires(post): coreutils

Obsoletes: rfkill < %{version}-%{release}
Provides: rfkill = %{version}-%{release}

%description
The util-linux package contains a large variety of low-level system
utilities that are necessary for a Linux system to function. Among
others, Util-linux contains the fdisk configuration tool and the login
program.

%package -n libsmartcols
Summary: Formatting library for ls-like programs.
Group: Development/Libraries
License: LGPLv2+

%description -n libsmartcols
This is library for ls-like terminal programs, part of util-linux.

%package -n libsmartcols-devel
Summary: Formatting library for ls-like programs.
Group: Development/Libraries
License: LGPLv2+
Requires: libsmartcols = %{version}-%{release}
Requires: pkgconfig

%description -n libsmartcols-devel
This is development library and headers for ls-like terminal programs,
part of util-linux.

%package -n libmount
Summary: Device mounting library
Group: Development/Libraries
License: LGPLv2+
Requires: libblkid = %{version}-%{release}
Requires: libuuid = %{version}-%{release}
Conflicts: filesystem < 3

%description -n libmount
This is the device mounting library, part of util-linux.

%package -n libmount-devel
Summary: Device mounting library
Group: Development/Libraries
License: LGPLv2+
Requires: libmount = %{version}-%{release}

%description -n libmount-devel
This is the device mounting development library and headers,
part of util-linux.

%package -n libblkid
License:        LGPLv2+
Summary:        Block device ID library
Group:          System/Libraries
Requires:       libuuid = %{version}-%{release}
Requires(post): coreutils

%description -n libblkid
This is block device identification library, part of util-linux.

%package -n libblkid-devel
License:        LGPLv2+
Summary:        Block device ID library
Group:          Development/Libraries
Requires:       libblkid = %{version}

%description -n libblkid-devel
This is the block device identification development library and headers,
part of util-linux.

%package -n libfdisk
Summary: Partitioning library for fdisk-like programs.
Group: Development/Libraries
License: LGPLv2+

%description -n libfdisk
This is library for fdisk-like programs, part of util-linux.

%package -n libfdisk-devel
Summary:  Partitioning library for fdisk-like programs.
Group: Development/Libraries
License: LGPLv2+
Requires: libfdisk = %{version}-%{release}

%description -n libfdisk-devel
This is development library and headers for fdisk-like programs,
part of util-linux.

%package -n libuuid
License:        BSD
Summary:        Universally unique ID library
Group:          System/Libraries

%description -n libuuid
This is the universally unique ID library, part of e2fsprogs.

The libuuid library generates and parses 128-bit universally unique
id's (UUID's).  A UUID is an identifier that is unique across both
space and time, with respect to the space of all UUIDs.  A UUID can
be used for multiple purposes, from tagging objects with an extremely
short lifetime, to reliably identifying very persistent objects
across a network.

See also the "uuid" package, which is a separate implementation.

%package -n libuuid-devel
License:        BSD
Summary:        Universally unique ID library
Group:          Development/Libraries
Requires:       libuuid = %{version}-%{release}
Provides:       libuuid-static = %{version}-%{release}

%description -n libuuid-devel
This is the universally unique ID development library and headers,
part of e2fsprogs.

The libuuid library generates and parses 128-bit universally unique
id's (UUID's).  A UUID is an identifier that is unique across both
space and time, with respect to the space of all UUIDs.  A UUID can
be used for multiple purposes, from tagging objects with an extremely
short lifetime, to reliably identifying very persistent objects
across a network.

See also the "uuid-devel" package, which is a separate implementation.

%package -n uuidd
License:        GPLv2+
Summary:        Helper daemon to guarantee uniqueness of time-based UUIDs
Group:          System/Daemons
Requires:       libuuid = %{version}-%{release}
Requires(pre): shadow-utils

%description -n uuidd
The uuidd package contains a userspace daemon (uuidd) which guarantees
uniqueness of time-based UUID generation even at very high rates on
SMP systems.

%package doc
Summary:   Documentation for %{name}
Group:     Documentation
Requires:  %{name} = %{version}-%{release}
Obsoletes: %{name}-docs

%description doc
Man and info pages for %{name}.


%prep
%setup -q -n %{name}-%{version}/%{name}

%build
# Because .git dir isn't included in tar_git, we explicitly state
# the version here.
echo %{version} | cut -d '+' -f 1 > .tarball-version

unset LINGUAS || :

export CFLAGS="-D_LARGEFILE_SOURCE -D_LARGEFILE64_SOURCE -D_FILE_OFFSET_BITS=64 %{optflags}"
export SUID_CFLAGS="-fpie"
export SUID_LDFLAGS="-pie"
./autogen.sh
%configure \
	--with-systemdsystemunitdir=no \
	--bindir=/bin \
	--sbindir=/sbin \
	--disable-wall \
	--enable-partx \
	--enable-kill \
	--enable-chfn-chsh \
	--enable-write \
	--with-utempter \
	--without-python \
	--disable-bash-completion \
	--disable-makeinstall-chown

# build util-linux
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/{bin,sbin}
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_infodir}
mkdir -p %{buildroot}%{_mandir}/man{1,6,8,5}
mkdir -p %{buildroot}%{_sbindir}
mkdir -p %{buildroot}%{_sysconfdir}/{pam.d,security/console.apps,blkid}
mkdir -p %{buildroot}%{_localstatedir}/log

# install util-linux
%make_install

# PAM settings
{
	pushd %{buildroot}%{_sysconfdir}/pam.d
	install -m 644 %{SOURCE1} ./login
	install -m 644 %{SOURCE2} ./remote
	install -m 644 %{SOURCE3} ./chsh
	install -m 644 %{SOURCE3} ./chfn
	install -m 644 %{SOURCE11} ./su
	install -m 644 %{SOURCE12} ./su-l
	install -m 644 %{SOURCE14} ./runuser
	install -m 644 %{SOURCE15} ./runuser-l
	popd
}

ln -sf ../../sbin/hwclock %{buildroot}%{_sbindir}/hwclock
ln -sf hwclock %{buildroot}/sbin/clock

# And a dirs uuidd needs that the makefiles don't create
install -d %{buildroot}%{_localstatedir}/run/uuidd
install -d %{buildroot}%{_localstatedir}/lib/libuuid

# remove libtool junk
rm -f %{buildroot}%{_prefix}/lib/libblkid.la

# libtool installs all libraries to --libdir=/lib, but we need
# devel stuff in /usr/lib  (TODO)
rm -f %{buildroot}/%{_lib}/libblkid.so
#mv %{buildroot}/%{_lib}/libblkid.a %{buildroot}%{_libdir}/
#ln -sf ../../%{_lib}/libblkid.so.1 %{buildroot}%{_libdir}/libblkid.so

# deprecated commands
for I in /sbin/mkfs.bfs /usr/sbin/sln \
	/usr/bin/chkdupexe %{_bindir}/line %{_bindir}/pg %{_bindir}/newgrp \
	/usr/sbin/shutdown /usr/sbin/vipw /usr/sbin/vigr; do
	rm -f $RPM_BUILD_ROOT$I
done

# deprecated man pages
for I in man1/chkdupexe.1 man1/line.1 man1/pg.1 man1/newgrp.1 \
	man8/mkfs.bfs.8 man8/vipw.8 man8/vigr; do
	rm -rf $RPM_BUILD_ROOT%{_mandir}/${I}*
done

# deprecated docs
for I in floppy-%{floppyver}/README.html; do
	rm -rf $I
done

ln -sf ../../bin/kill %{buildroot}%{_bindir}/kill

# /usr/sbin -> /sbin
for I in addpart delpart partx; do
	if [ -e %{buildroot}%{_sbindir}/$I ]; then
		mv %{buildroot}%{_sbindir}/$I %{buildroot}/sbin/$I
	fi
done

# /usr/bin -> /bin
for I in taskset; do
	if [ -e %{buildroot}%{_bindir}/$I ]; then
		mv %{buildroot}%{_bindir}/$I %{buildroot}/bin/$I
	fi
done

# /sbin -> /bin
for I in raw; do
	if [ -e %{buildroot}/sbin/$I ]; then
		mv %{buildroot}/sbin/$I %{buildroot}/bin/$I
	fi
done

ln -s /proc/self/mounts %{buildroot}/etc/mtab

# find MO files
%find_lang %{name}

rm -f %{buildroot}%{_infodir}/dir

mkdir -p %{buildroot}%{_docdir}/%{name}-%{version}
install -m0644 -t %{buildroot}%{_docdir}/%{name}-%{version} \
        AUTHORS README NEWS
mv %{buildroot}%{_docdir}/util-linux/getopt \
   %{buildroot}%{_docdir}/%{name}-%{version}/getopt
rmdir %{buildroot}%{_docdir}/util-linux

# create list of setarch(8) symlinks
rm -f symlinks.list
find  %{buildroot}%{_bindir}/ -type l \
	| grep -E ".*(linux32|linux64|s390|s390x|i386|ppc|ppc64|ppc32|sparc|sparc64|sparc32|sparc32bash|mips|mips64|mips32|ia64|x86_64)$" \
	| sed 's|^'%{buildroot}'||' >> symlinks.list

rm -f documentation.list
find  %{buildroot}%{_mandir}/man8 \
	| grep -E ".*(linux32|linux64|s390|s390x|i386|ppc|ppc64|ppc32|sparc|sparc64|sparc32|sparc32bash|mips|mips64|mips32|ia64|x86_64)\.8.*" \
	| sed -e 's|^'%{buildroot}'||' -e 's/$/*/' >> documentation.list

%post
# NOTE: /var/log/lastlog is owned (%ghost) by setup package
# however it is created here as setup can not depend on the packages
# that have the tools to create the file.
# only for minimal buildroots without /var/log
[ -d /var/log ] || mkdir -p /var/log
touch /var/log/lastlog
chown root:root /var/log/lastlog
chmod 0644 /var/log/lastlog
/sbin/ldconfig

# Make sure mtab points to right place.
rm -f /etc/mtab
ln -s /proc/self/mounts /etc/mtab

%post -n libblkid
/sbin/ldconfig

### Move blkid cache to /run
[ -d /run/blkid ] || mkdir -p /run/blkid
for I in /etc/blkid.tab /etc/blkid.tab.old \
         /etc/blkid/blkid.tab /etc/blkid/blkid.tab.old; do

	if [ -f "$I" ]; then
		mv "$I" /run/blkid/ || :
	fi
done

%postun -n libblkid -p /sbin/ldconfig

%post -n libfdisk -p /sbin/ldconfig
%postun -n libfdisk -p /sbin/ldconfig

%post -n libuuid -p /sbin/ldconfig
%postun -n libuuid -p /sbin/ldconfig

%post -n libmount -p /sbin/ldconfig
%postun -n libmount -p /sbin/ldconfig

%post -n libsmartcols -p /sbin/ldconfig
%postun -n libsmartcols -p /sbin/ldconfig

%pre -n uuidd
getent group uuidd >/dev/null || groupadd -r uuidd
getent passwd uuidd >/dev/null || \
useradd -r -g uuidd -d /var/lib/libuuid -s /sbin/nologin \
    -c "UUID generator helper daemon" uuidd
exit 0

%lang_package

%files -f symlinks.list
%defattr(-,root,root)
%license Documentation/licenses/*

%config(noreplace)	%{_sysconfdir}/pam.d/chfn
%config(noreplace)	%{_sysconfdir}/pam.d/chsh
%config(noreplace)	%{_sysconfdir}/pam.d/login
%config(noreplace)	%{_sysconfdir}/pam.d/remote
%config(noreplace)	%{_sysconfdir}/pam.d/su
%config(noreplace)	%{_sysconfdir}/pam.d/su-l
%config(noreplace)      %{_sysconfdir}/pam.d/runuser
%config(noreplace)      %{_sysconfdir}/pam.d/runuser-l

%ghost %verify(not md5 size mtime) %config(noreplace,missingok) /etc/mtab

/bin/dmesg
%attr(4755,root,root)	/bin/mount
%attr(4755,root,root)	/bin/umount
%attr(4755,root,root)	/bin/su
%attr(755,root,root)	/bin/login
%attr(4711,root,root)	%{_bindir}/chfn
%attr(4711,root,root)	%{_bindir}/chsh
%attr(2755,root,tty)	%{_bindir}/write
/bin/more
/bin/kill
%{_bindir}/last
%{_bindir}/lastb
/bin/taskset
/bin/findmnt
/bin/lsblk
%{_bindir}/lscpu
%{_bindir}/lsipc
%{_bindir}/lslogins
%{_bindir}/lsmem
%{_bindir}/lsns
/bin/mountpoint
%{_bindir}/mesg
%{_bindir}/nsenter
%{_bindir}/prlimit
%{_bindir}/uname26

/sbin/agetty
/sbin/blkdiscard
/sbin/blockdev
/sbin/pivot_root
/sbin/ctrlaltdel
/sbin/addpart
/sbin/delpart
/sbin/partx
/sbin/fsfreeze
/sbin/fstrim
/sbin/swaplabel
/sbin/wipefs
%{_bindir}/ipcmk
%{_bindir}/fallocate
%{_bindir}/fincore
%{_bindir}/unshare

%ifnarch %no_cfsfdisk_archs
/sbin/sfdisk
/sbin/cfdisk
%endif

/bin/raw
/bin/wdctl
/sbin/chcpu
/sbin/fdisk
/sbin/clock
/sbin/hwclock
%{_sbindir}/hwclock
/sbin/mkfs
/sbin/mkfs.minix
/sbin/mkswap
/sbin/nologin
/sbin/runuser
/sbin/sulogin

%{_bindir}/chrt
%{_bindir}/ionice

%{_bindir}/cal
%{_bindir}/col
%{_bindir}/colcrt
%{_bindir}/colrm
%{_bindir}/column
%{_bindir}/chmem
%{_sbindir}/fdformat
%{_sbindir}/resizepart
%{_sbindir}/rfkill
%{_bindir}/flock
%{_bindir}/getopt
%{_bindir}/hexdump
%{_bindir}/ipcrm
%{_bindir}/ipcs
%{_bindir}/isosize
%{_bindir}/kill
%{_bindir}/logger
%{_bindir}/look
%{_bindir}/mcookie
/sbin/fsck
/sbin/fsck.cramfs
/sbin/fsck.minix
/sbin/mkfs.cramfs
%{_bindir}/namei
%{_bindir}/rename
%{_bindir}/renice
%{_bindir}/rev
%{_bindir}/script
%{_bindir}/scriptreplay
%{_bindir}/setarch
%{_bindir}/setsid
%{_bindir}/setterm
%{_bindir}/ul
%{_bindir}/uuidgen
%{_bindir}/uuidparse
%{_bindir}/eject
%{_bindir}/lslocks
%{_bindir}/utmpdump
%{_bindir}/whereis

%{_sbindir}/readprofile
%{_sbindir}/rtcwake
%{_sbindir}/ldattach
/sbin/swapon
/sbin/swapoff
/sbin/switch_root
/sbin/losetup
/sbin/blkid
/sbin/findfs
/sbin/zramctl
%{_bindir}/choom

%files -n uuidd
%defattr(-,root,root)
%license Documentation/licenses/COPYING.GPL-2.0-or-later
%attr(-, uuidd, uuidd) %{_sbindir}/uuidd
%dir %attr(2775, uuidd, uuidd) /var/lib/libuuid
%dir %attr(2775, uuidd, uuidd) /var/run/uuidd

%files -n libsmartcols
%defattr(-,root,root)
%license Documentation/licenses/COPYING.LGPL-2.1-or-later libsmartcols/COPYING
%{_libdir}/libsmartcols.so.*

%files -n libsmartcols-devel
%defattr(-,root,root)
%{_libdir}/libsmartcols.so
%{_includedir}/libsmartcols
%{_libdir}/pkgconfig/smartcols.pc

%files -n libmount
%defattr(-,root,root)
%license libmount/COPYING
%{_libdir}/libmount.so.*

%files -n libmount-devel
%defattr(-,root,root)
%{_libdir}/libmount.so
%{_includedir}/libmount
%{_libdir}/pkgconfig/mount.pc

%files -n libblkid
%defattr(-,root,root)
%license libblkid/COPYING
%{_libdir}/libblkid.so.*

%files -n libblkid-devel
%defattr(-,root,root)
%{_libdir}/libblkid.so
%{_includedir}/blkid
%{_libdir}/pkgconfig/blkid.pc

%files -n libfdisk
%defattr(-,root,root)
%license libfdisk/COPYING
%{_libdir}/libfdisk.so.*

%files -n libfdisk-devel
%defattr(-,root,root)
%{_libdir}/libfdisk.so
%{_includedir}/libfdisk
%{_libdir}/pkgconfig/fdisk.pc

%files -n libuuid
%defattr(-,root,root)
%license libuuid/COPYING
%{_libdir}/libuuid.so.*

%files -n libuuid-devel
%defattr(-,root,root)
%{_libdir}/libuuid.so
%{_includedir}/uuid
%{_libdir}/pkgconfig/uuid.pc

%files doc -f documentation.list
%defattr(-,root,root)
%{_docdir}/%{name}-%{version}

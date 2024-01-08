### Header
Name:           util-linux
Version:        2.38.1
Release:        1
License:        GPLv2 and GPLv2+ and BSD with advertising and Public Domain
Summary:        A collection of basic system utilities
Url:            https://github.com/sailfishos/util-linux
BuildRequires:  libtool
BuildRequires:  gettext-devel
BuildRequires:  pam-devel
BuildRequires:  texinfo
BuildRequires:  pkgconfig(ext2fs) >= 1.36
BuildRequires:  pkgconfig(ncursesw)
BuildRequires:  pkgconfig(popt)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  pkgconfig(libcrypt)
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
# docs no longer generated due to needing lots of dependencies via rubygem-asciidoctor
Obsoletes: util-linux-doc <= 2.38.1
Provides: util-linux-doc = %{version}-%{release}

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
License: LGPLv2+

%description -n libsmartcols
This is library for ls-like terminal programs, part of util-linux.

%package -n libsmartcols-devel
Summary: Formatting library for ls-like programs.
License: LGPLv2+
Requires: libsmartcols = %{version}-%{release}
Requires: pkgconfig

%description -n libsmartcols-devel
This is development library and headers for ls-like terminal programs,
part of util-linux.

%package -n libmount
Summary: Device mounting library
License: LGPLv2+
Requires: libblkid = %{version}-%{release}
Requires: libuuid = %{version}-%{release}

%description -n libmount
This is the device mounting library, part of util-linux.

%package -n libmount-devel
Summary: Device mounting library
License: LGPLv2+
Requires: libmount = %{version}-%{release}

%description -n libmount-devel
This is the device mounting development library and headers,
part of util-linux.

%package -n libblkid
License:        LGPLv2+
Summary:        Block device ID library
Requires:       libuuid = %{version}-%{release}
Requires(post): coreutils

%description -n libblkid
This is block device identification library, part of util-linux.

%package -n libblkid-devel
License:        LGPLv2+
Summary:        Block device ID library
Requires:       libblkid = %{version}

%description -n libblkid-devel
This is the block device identification development library and headers,
part of util-linux.

%package -n libfdisk
Summary: Partitioning library for fdisk-like programs.
License: LGPLv2+

%description -n libfdisk
This is library for fdisk-like programs, part of util-linux.

%package -n libfdisk-devel
Summary:  Partitioning library for fdisk-like programs.
License: LGPLv2+
Requires: libfdisk = %{version}-%{release}

%description -n libfdisk-devel
This is development library and headers for fdisk-like programs,
part of util-linux.

%package -n libuuid
License:        BSD
Summary:        Universally unique ID library


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
Requires:       libuuid = %{version}-%{release}
Requires(pre): shadow-utils

%description -n uuidd
The uuidd package contains a userspace daemon (uuidd) which guarantees
uniqueness of time-based UUID generation even at very high rates on
SMP systems.

%package -n cfdisk
License:        GPLv2+
Summary:        cfdisk is a curses-based program for partitioning any block device

%description -n cfdisk
%{summary}.

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
	--bindir=/usr/bin \
	--sbindir=/usr/sbin \
	--disable-bfs \
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
%make_build

%install
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

ln -sf hwclock %{buildroot}/%{_sbindir}/clock

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


ln -s ../proc/self/mounts %{buildroot}/etc/mtab

# remove static libs
rm -f $RPM_BUILD_ROOT%{_libdir}/lib{uuid,blkid,mount,smartcols,fdisk}.a

# find MO files
%find_lang %{name}

rm -f %{buildroot}%{_infodir}/dir

# remove the random getopt usage example files
rm -f ${RPM_BUILD_ROOT}%{_datadir}/doc/util-linux/getopt*

# create list of setarch(8) symlinks
rm -f symlinks.list
find  %{buildroot}%{_bindir}/ -type l \
	| grep -E ".*(linux32|linux64|s390|s390x|i386|ppc|ppc64|ppc32|sparc|sparc64|sparc32|sparc32bash|mips|mips64|mips32|ia64|x86_64)$" \
	| sed 's|^'%{buildroot}'||' >> symlinks.list

# FIXME: Remove after UsrMove
ln -sf %{_sbindir}/nologin %{buildroot}/sbin/nologin
ln -sf %{_bindir}/su %{buildroot}/bin/su
ln -sf %{_bindir}/mount %{buildroot}/bin/mount


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
useradd -r -g uuidd -d /var/lib/libuuid -s %{_sbindir}/nologin \
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

%{_bindir}/dmesg
%attr(4755,root,root)	%{_bindir}/mount
# FIXME: Remove after UsrMove
%attr(4755,root,root)	/bin/mount
%attr(4755,root,root)	%{_bindir}/umount
%attr(4755,root,root)	%{_bindir}/su
# FIXME: Remove after UsrMove
%attr(4755,root,root)	/bin/su
%attr(755,root,root)	%{_bindir}/login
%attr(4711,root,root)	%{_bindir}/chfn
%attr(4711,root,root)	%{_bindir}/chsh
%attr(2755,root,tty)	%{_bindir}/write
%{_bindir}/more
%{_bindir}/kill
%{_bindir}/last
%{_bindir}/lastb
%{_bindir}/taskset
%{_bindir}/findmnt
%{_bindir}/lsblk
%{_bindir}/lscpu
%{_bindir}/lsipc
%{_bindir}/lsirq
%{_bindir}/lslogins
%{_bindir}/lsmem
%{_bindir}/lsns
%{_bindir}/mountpoint
%{_bindir}/mesg
%{_bindir}/nsenter
%{_bindir}/prlimit
%{_bindir}/uname26

%{_sbindir}/agetty
%{_sbindir}/blkdiscard
%{_sbindir}/blockdev
%{_sbindir}/pivot_root
%{_sbindir}/ctrlaltdel
%{_sbindir}/addpart
%{_sbindir}/delpart
%{_sbindir}/partx
%{_sbindir}/fsfreeze
%{_sbindir}/fstrim
%{_sbindir}/swaplabel
%{_sbindir}/wipefs
%{_bindir}/ipcmk
%{_bindir}/fallocate
%{_bindir}/fincore
%{_bindir}/unshare
%{_sbindir}/sfdisk

%{_sbindir}/raw
%{_bindir}/wdctl
%{_sbindir}/chcpu
%{_sbindir}/fdisk
%{_sbindir}/clock
%{_sbindir}/hwclock
%{_sbindir}/hwclock
%{_sbindir}/mkfs
%{_sbindir}/mkfs.minix
%{_sbindir}/mkswap
# FIXME: Remove after UsrMove
/sbin/nologin
%{_sbindir}/nologin
%{_sbindir}/runuser
%{_sbindir}/sulogin

%{_bindir}/chrt
%{_bindir}/ionice
%{_bindir}/hardlink
%{_bindir}/cal
%{_bindir}/col
%{_bindir}/colcrt
%{_bindir}/colrm
%{_bindir}/column
%{_bindir}/chmem
%{_sbindir}/resizepart
%{_sbindir}/rfkill
%{_bindir}/flock
%{_bindir}/getopt
%{_bindir}/hexdump
%{_bindir}/ipcrm
%{_bindir}/ipcs
%{_bindir}/irqtop
%{_bindir}/isosize
%{_bindir}/kill
%{_bindir}/logger
%{_bindir}/look
%{_bindir}/mcookie
%{_sbindir}/fsck
%{_sbindir}/fsck.cramfs
%{_sbindir}/fsck.minix
%{_sbindir}/mkfs.cramfs
%{_bindir}/namei
%{_bindir}/rename
%{_bindir}/renice
%{_bindir}/rev
%{_bindir}/script
%{_bindir}/scriptlive
%{_bindir}/scriptreplay
%{_bindir}/setarch
%{_bindir}/setsid
%{_bindir}/setterm
%{_bindir}/uclampset
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
%{_sbindir}/swapon
%{_sbindir}/swapoff
%{_sbindir}/switch_root
%{_sbindir}/losetup
%{_sbindir}/blkid
%{_sbindir}/findfs
%{_sbindir}/zramctl
%{_bindir}/choom
/etc/mtab

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

%files -n cfdisk
%defattr(-,root,root)
%{_sbindir}/cfdisk

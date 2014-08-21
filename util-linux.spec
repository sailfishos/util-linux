### Header
Name:           util-linux
Version:        2.22.2
Release:        1
License:        GPLv2 and GPLv2+ and BSD with advertising and Public Domain
Summary:        A collection of basic system utilities
Url:            http://kernel.org/~kzak/util-linux/
Group:          System/Base

### Macros
%define whichver 2.17
%define no_cfsfdisk_archs sparc sparcv9 sparc64
%define cytune_archs %{ix86} alpha armv4l

BuildRequires:  gettext-devel
BuildRequires:  pam-devel
BuildRequires:  texinfo
### Dependences
BuildRequires:  pkgconfig(ext2fs) >= 1.36
BuildRequires:  pkgconfig(ncurses)
BuildRequires:  pkgconfig(popt)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  libutempter-devel

### Sources
Source0:        ftp://ftp.kernel.org/pub/linux/utils/util-linux/v2.21/util-linux-%{version}.tar.xz
Source1:        util-linux-login.pamd
Source2:        util-linux-remote.pamd
Source3:        util-linux-chsh-chfn.pamd
Source4:        util-linux-60-raw.rules
Source8:        nologin.c
Source9:        nologin.8
Source10:       http://ftp.gnu.org/gnu/which/which-%{whichver}.tar.gz
Source11:       util-linux-su.pamd
Source12:       util-linux-su-l.pamd

### Obsoletes & Conflicts & Provides
# old versions of e2fsprogs contain fsck, uuidgen
Conflicts: e2fsprogs <= 1.42.2
# rename from util-linux-ng back to util-linux
Obsoletes: util-linux-ng <= 2.20.1
Provides: util-linux-ng = %{version}-%{release}
Conflicts: filesystem < 3

Patch0:         util-linux-2.21.2-config-option-lscpu-prlimit.patch
Patch1:         mbsalign-license.patch

Requires:       /etc/pam.d/system-auth
Requires:       pam >= 0.66-4
Obsoletes:      which
Provides:       which
Provides:       mount
Requires: libuuid = %{version}-%{release}
Requires: libblkid = %{version}-%{release}
Requires(post): coreutils

%description
The util-linux package contains a large variety of low-level system
utilities that are necessary for a Linux system to function. Among
others, Util-linux contains the fdisk configuration tool and the login
program.

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
License:        GPLv2
Summary:        Helper daemon to guarantee uniqueness of time-based UUIDs
Group:          System/Daemons
Requires:       libuuid = %{version}-%{release}
Requires(pre): shadow-utils

%description -n uuidd
The uuidd package contains a userspace daemon (uuidd) which guarantees
uniqueness of time-based UUID generation even at very high rates on
SMP systems.


%prep
%setup -q -b 10 -n %{name}-%{version}
cp %{SOURCE8} %{SOURCE9} .

%patch0 -p1
%patch1 -p1

# GPLv3 files remove those to be sure those are not used.
# Not removed as not ending to binaries: rm -rf tests/ts/lscpu/lscpu tools/git-version-gen 
# WARNING WARNING!!! fdisk and partx use this as well...
# rm -rf lib/mbsalign.c
# NOTE: mbsalign-license.patch fixes this.

%build
unset LINGUAS || :

export CFLAGS="-D_LARGEFILE_SOURCE -D_LARGEFILE64_SOURCE -D_FILE_OFFSET_BITS=64 %{optflags}"
export SUID_CFLAGS="-fpie"
export SUID_LDFLAGS="-pie"
./autogen.sh
%configure \
	--bindir=/bin \
	--sbindir=/sbin \
	--disable-wall \
	--disable-lscpu \
	--disable-prlimit \
	--enable-partx \
	--enable-login-utils \
	--enable-kill \
	--enable-chfn-chsh \
	--enable-write \
	--enable-new-mount \
	--with-utempter \
	--disable-makeinstall-chown

# build util-linux
make %{?_smp_mflags}

# build nologin
gcc $CFLAGS -o nologin nologin.c

cd ..
cd which-%{whichver}
%configure

make %{?_smp_mflags}


%install
mkdir -p %{buildroot}/{bin,sbin}
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_infodir}
mkdir -p %{buildroot}%{_mandir}/man{1,6,8,5}
mkdir -p %{buildroot}%{_sbindir}
mkdir -p %{buildroot}%{_sysconfdir}/{pam.d,security/console.apps,blkid}
mkdir -p %{buildroot}%{_localstatedir}/log
touch %{buildroot}%{_localstatedir}/log/lastlog
chmod 0644 %{buildroot}%{_localstatedir}/log/lastlog

# install util-linux
%make_install

# install nologin
install -m 755 nologin %{buildroot}/sbin
install -m 644 nologin.8 %{buildroot}%{_mandir}/man8

# PAM settings
{
	pushd %{buildroot}%{_sysconfdir}/pam.d
	install -m 644 %{SOURCE1} ./login
	install -m 644 %{SOURCE2} ./remote
	install -m 644 %{SOURCE3} ./chsh
	install -m 644 %{SOURCE3} ./chfn
	install -m 644 %{SOURCE11} ./su
	install -m 644 %{SOURCE12} ./su-l
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

# Final cleanup
%ifnarch %cytune_archs
rm -f %{buildroot}%{_bindir}/cytune %{buildroot}%{_mandir}/man8/cytune.8*
%endif

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

# we install getopt/getopt-*.{bash,tcsh} as doc files
#chmod 644 getopt/getopt-*.{bash,tcsh}
rm -f %{buildroot}%{_datadir}/getopt/*
rmdir %{buildroot}%{_datadir}/getopt

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



cd ..
# which install
cd which-%{whichver}
%make_install
mkdir -p %{buildroot}%{_defaultdocdir}/which
install -m 0644 README    %{buildroot}%{_defaultdocdir}/which/
install -m 0644 EXAMPLES  %{buildroot}%{_defaultdocdir}/which/
install -m 0644 README.alias %{buildroot}%{_defaultdocdir}/which/

rm -f %{buildroot}%{_infodir}/dir

cd ../%{name}-%{version}
# create list of setarch(8) symlinks
find  %{buildroot}%{_bindir}/ -regextype posix-egrep -type l \
	-regex ".*(linux32|linux64|s390|s390x|i386|ppc|ppc64|ppc32|sparc|sparc64|sparc32|sparc32bash|mips|mips64|mips32|ia64|x86_64)$" \
	-printf "%{_bindir}/%f\n" >> documentation.list

find  %{buildroot}%{_mandir}/man8 -regextype posix-egrep  \
	-regex ".*(linux32|linux64|s390|s390x|i386|ppc|ppc64|ppc32|sparc|sparc64|sparc32|sparc32bash|mips|mips64|mips32|ia64|x86_64)\.8.*" \
	-printf "%{_mandir}/man8/%f*\n" >> documentation.list

%post
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

%post -n libuuid -p /sbin/ldconfig
%postun -n libuuid -p /sbin/ldconfig

%pre -n uuidd
getent group uuidd >/dev/null || groupadd -r uuidd
getent passwd uuidd >/dev/null || \
useradd -r -g uuidd -d /var/lib/libuuid -s /sbin/nologin \
    -c "UUID generator helper daemon" uuidd
exit 0

%lang_package

%docs_package

%files
%defattr(-,root,root)
%doc AUTHORS Documentation/licenses/*

%config(noreplace)	%{_sysconfdir}/pam.d/chfn
%config(noreplace)	%{_sysconfdir}/pam.d/chsh
%config(noreplace)	%{_sysconfdir}/pam.d/login
%config(noreplace)	%{_sysconfdir}/pam.d/remote
%config(noreplace)	%{_sysconfdir}/pam.d/su
%config(noreplace)	%{_sysconfdir}/pam.d/su-l

%ghost %attr(0644,root,root) %verify(not md5 size mtime) /var/log/lastlog
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
/bin/taskset
/bin/findmnt
/bin/lsblk
/bin/mountpoint

%{_defaultdocdir}/which/

%{_bindir}/which

/sbin/agetty
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
/sbin/sulogin

%{_bindir}/chrt
%{_bindir}/ionice

%{_bindir}/cal
%{_bindir}/col
%{_bindir}/colcrt
%{_bindir}/colrm
%{_bindir}/column
%ifarch %cytune_archs
%{_bindir}/cytune
%endif
%{_sbindir}/fdformat
%{_sbindir}/resizepart
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
%{_bindir}/tailf
%{_bindir}/ul
%{_bindir}/uuidgen
%{_bindir}/eject
%{_bindir}/lslocks
%{_bindir}/utmpdump
%{_bindir}/whereis

%{_sbindir}/readprofile
%{_sbindir}/tunelp
%{_sbindir}/rtcwake
%{_sbindir}/ldattach
/sbin/swapon
/sbin/swapoff
/sbin/switch_root
/sbin/losetup
/sbin/blkid
/sbin/findfs

%files -n uuidd
%defattr(-,root,root)
%doc Documentation/licenses/COPYING.GPLv2
%attr(-, uuidd, uuidd) %{_sbindir}/uuidd
%dir %attr(2775, uuidd, uuidd) /var/lib/libuuid
%dir %attr(2775, uuidd, uuidd) /var/run/uuidd

%files -n libblkid
%defattr(-,root,root)
%doc libblkid/COPYING
%{_libdir}/libblkid.so.*
#libmount
%doc libmount/COPYING
%{_libdir}/libmount.so.*

%files -n libblkid-devel
%defattr(-,root,root)
%doc libblkid/COPYING
%{_libdir}/libblkid.so
%{_includedir}/blkid
%{_mandir}/man3/libblkid.3*
%{_libdir}/pkgconfig/blkid.pc
# libmount
%doc libmount/COPYING
%{_libdir}/libmount.so
%{_includedir}/libmount
%{_libdir}/pkgconfig/mount.pc

%files -n libuuid
%defattr(-,root,root)
%doc libuuid/COPYING
%{_libdir}/libuuid.so.*

%files -n libuuid-devel
%defattr(-,root,root)
%doc libuuid/COPYING
%{_libdir}/libuuid.so
%{_includedir}/uuid
%{_libdir}/pkgconfig/uuid.pc


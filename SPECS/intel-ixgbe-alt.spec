%define vendor_name Intel
%define vendor_label intel
%define driver_name ixgbe

# XCP-ng: install to the override directory
%define module_dir override

Summary: %{vendor_name} %{driver_name} device drivers
Name: %{vendor_label}-%{driver_name}-alt
Version: 5.9.4
Release: 3%{?dist}
# Built against new kABI after cip rebase
Requires: xcpng-kernel-kabi = 4.19.325-cip134+

License: GPL

# Downloaded from https://downloadcenter.intel.com/download/14687/Intel-Network-Adapter-Driver-for-PCIe-Intel-10-Gigabit-Ethernet-Network-Connections-under-Linux-
Source0: ixgbe-%{version}.tar.gz

Patch1000: 0001-intel-ixgbe-alt-compat-handle-newer-kernels-with-skb.patch

BuildRequires: gcc
BuildRequires: kernel-devel
Provides: vendor-driver
Requires: kernel-uname-r = %{kernel_version}
Requires(post): /usr/sbin/depmod
Requires(postun): /usr/sbin/depmod

%description
%{vendor_name} %{driver_name} device drivers for the Linux Kernel
version %{kernel_version}.

%prep
%autosetup -p1 -n ixgbe-%{version}

%build
%{?cov_wrap} %{make_build} -C /lib/modules/%{kernel_version}/build M=$(pwd)/src KSRC=/lib/modules/%{kernel_version}/build modules

%install
%{?cov_wrap} %{__make} %{?_smp_mflags} -C /lib/modules/%{kernel_version}/build M=$(pwd)/src INSTALL_MOD_PATH=%{buildroot} INSTALL_MOD_DIR=%{module_dir} DEPMOD=/bin/true modules_install

# mark modules executable so that strip-to-file can strip them
find %{buildroot}/lib/modules/%{kernel_version} -name "*.ko" -type f | xargs chmod u+x

%post
/sbin/depmod %{kernel_version}
%{regenerate_initrd_post}

%postun
/sbin/depmod %{kernel_version}
%{regenerate_initrd_postun}

%posttrans
%{regenerate_initrd_posttrans}

%files
/lib/modules/%{kernel_version}/*/*.ko

%changelog
* Mon Aug 31 2026 Quentin Casasnovas <quentin.casasnovas@vates.tech> - 5.9.4-3
- Rebuild for kernel v4.19.325-cip134

* Fri Sep 16 2022 Samuel Verschelde <stormi-xcp@ylix.fr> - 5.9.4-2
- Rebuild for XCP-ng 8.3

* Fri Jan 08 2021 Samuel Verschelde <stormi-xcp@ylix.fr> - 5.9.4-1
- initial package, version 5.9.4

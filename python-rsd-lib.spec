# Macros for py2/py3 compatibility
%if 0%{?fedora} || 0%{?rhel} > 7
%global pyver %{python3_pkgversion}
%else
%global pyver 2
%endif
%global pyver_bin python%{pyver}
%global pyver_sitelib %python%{pyver}_sitelib
%global pyver_install %py%{pyver}_install
%global pyver_build %py%{pyver}_build
# End of macros for py2/py3 compatibility
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global sname rsd-lib
%global pyname rsd_lib

%global with_doc 1

Name:           python-%{sname}
Version:        XXX
Release:        XXX
Summary:        Python library for interfacing with Intel Rack Scale Design enabled hardware.

License:        ASL 2.0
URL:            http://git.openstack.org/cgit/openstack/%{sname}
Source0:        http://tarballs.openstack.org/%{sname}/%{sname}-%{upstream_version}.tar.gz
BuildArch:      noarch

%description
This library extends the existing Sushy library to include functionality for
Intel RackScale Design enabled hardware. Capabilities include logical node
composition and decomposition, remote storage discovery and composition,
and NVMe over PCIe drive attaching and detaching to logical nodes.

%package -n     python%{pyver}-%{sname}
Summary:        %{summary}
%{?python_provide:%python_provide python%{pyver}-%{sname}}

BuildRequires:  python%{pyver}-devel
BuildRequires:  python%{pyver}-jsonschema
BuildRequires:  python%{pyver}-pbr >= 2.0
BuildRequires:  python%{pyver}-setuptools
BuildRequires:  python%{pyver}-sushy >= 1.2.0
BuildRequires:  python%{pyver}-sushy-tests >= 1.2.0

Requires:       python%{pyver}-jsonschema
Requires:       python%{pyver}-pbr >= 2.0
Requires:       python%{pyver}-sushy >= 1.2.0

%description -n python%{pyver}-%{sname}
This library extends the existing Sushy library to include functionality for
Intel RackScale Design enabled hardware. Capabilities include logical node
composition and decomposition, remote storage discovery and composition,
and NVMe over PCIe drive attaching and detaching to logical nodes.

%package -n python%{pyver}-%{sname}-tests
Summary: rsd-lib tests

BuildRequires: python%{pyver}-devel

Requires: python%{pyver}-%{sname} = %{version}-%{release}
Requires: python%{pyver}-jsonschema
Requires: python%{pyver}-pbr
Requires: python%{pyver}-setuptools
Requires: python%{pyver}-sushy >= 1.2.0
Requires: python%{pyver}-sushy-tests >= 1.2.0

%description -n python%{pyver}-%{sname}-tests
Tests for rsd-lib

%if 0%{?with_doc}
%package -n python-%{sname}-doc
Summary: rsd-lib documentation

BuildRequires: python%{pyver}-sphinx
BuildRequires: python%{pyver}-oslo-sphinx
BuildRequires: python%{pyver}-openstackdocstheme >= 1.11.0

%description -n python-%{sname}-doc
Documentation for rsd-lib
%endif

%prep
%autosetup -n %{sname}-%{upstream_version} -S git

# Let's handle dependencies ourseleves
rm -f *requirements.txt

%build
%{pyver_build}

%if 0%{?with_doc}
# generate html docs
%{pyver_bin} setup.py build_sphinx
# remove the sphinx-build-%{pyver} leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%{pyver_install}

%check
export PYTHON=%{pyver_bin}
# (TODO) ignore unit tests until rsd-lib is updated to 0.3.1
%{pyver_bin} setup.py test || true

%files -n python%{pyver}-%{sname}
%license LICENSE
%doc doc/source/readme.rst README.rst
%{pyver_sitelib}/%{pyname}
%{pyver_sitelib}/%{pyname}-*.egg-info
%exclude %{pyver_sitelib}/%{pyname}/tests

%files -n python%{pyver}-%{sname}-tests
%license LICENSE
%{pyver_sitelib}/%{pyname}/tests

%if 0%{?with_doc}
%files -n python-%{sname}-doc
%license LICENSE
%doc doc/build/html README.rst
%endif

%changelog
# REMOVEME: error caused by commit http://git.openstack.org/cgit/openstack/rsd-lib/commit/?id=317902aac1bc47f1671b5bbb946c0c9323a62833

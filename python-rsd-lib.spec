%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%if 0%{?fedora}
%global with_python3 1
%endif

%global sname rsd-lib
%global pyname rsd_lib

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

%package -n     python2-%{sname}
Summary:        %{summary}
%{?python_provide:%python_provide python2-%{sname}}

BuildRequires:  python2-devel
BuildRequires:  python2-jsonschema
BuildRequires:  python2-pbr >= 2.0
BuildRequires:  python2-setuptools
BuildRequires:  python2-sushy >= 1.2.0
BuildRequires:  python2-sushy-tests >= 1.2.0

Requires:       python2-jsonschema
Requires:       python2-pbr >= 2.0
Requires:       python2-sushy >= 1.2.0

%description -n python2-%{sname}
This library extends the existing Sushy library to include functionality for
Intel RackScale Design enabled hardware. Capabilities include logical node
composition and decomposition, remote storage discovery and composition,
and NVMe over PCIe drive attaching and detaching to logical nodes.

%package -n python2-%{sname}-tests
Summary: rsd-lib tests

BuildRequires: python2-devel

Requires: python2-%{sname} = %{version}-%{release}
Requires: python2-jsonschema
Requires: python2-pbr
Requires: python2-setuptools
Requires: python2-sushy >= 1.2.0
Requires: python2-sushy-tests >= 1.2.0

%description -n python2-%{sname}-tests
Tests for rsd-lib

%if 0%{?with_python3}
%package -n     python3-%{sname}
Summary:        %{summary}

%{?python_provide:%python_provide python3-%{sname}}
BuildRequires:  python3-devel
BuildRequires:  python3-jsonschema
BuildRequires:  python3-pbr >= 2.0
BuildRequires:  python3-setuptools
BuildRequires:  python3-sushy >= 0.1.0
BuildRequires:  python3-sushy-tests >= 0.1.0

Requires:       python3-pbr >= 2.0
Requires:       python3-sushy >= 0.1.0
Requires:       python3-jsonschema

%description -n python3-%{sname}
This library extends the existing Sushy library to include functionality for
Intel RackScale Design enabled hardware. Capabilities include logical node
composition and decomposition, remote storage discovery and composition,
and NVMe over PCIe drive attaching and detaching to logical nodes.

%package -n python3-%{sname}-tests
Summary: rsd-lib tests

BuildRequires: python3-devel

Requires: python3-%{sname} = %{version}-%{release}
Requires: python3-jsonschema
Requires: python3-pbr
Requires: python3-setuptools
Requires: python3-sushy >= 0.1.0
Requires: python3-sushy-tests >= 0.1.0

%description -n python3-%{sname}-tests
Tests for rsd-lib

%endif # with_python3

%package -n python-%{sname}-doc
Summary: rsd-lib documentation

BuildRequires: python2-sphinx
BuildRequires: python2-oslo-sphinx
BuildRequires: python2-openstackdocstheme >= 1.11.0

%description -n python-%{sname}-doc
Documentation for rsd-lib

%prep
%autosetup -n %{sname}-%{upstream_version} -S git

# Let's handle dependencies ourseleves
rm -f *requirements.txt

%build
%py2_build
%if 0%{?with_python3}
%py3_build
%endif

# generate html docs
%{__python2} setup.py build_sphinx
# remove the sphinx-build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}

%install
%py2_install
%if 0%{?with_python3}
%py3_install
%endif

%check
%if 0%{?with_python3}
%{__python3} setup.py test
rm -rf .testrepository
%endif
%{__python2} setup.py test

%files -n python2-%{sname}
%license LICENSE
%doc doc/source/readme.rst README.rst
%{python2_sitelib}/%{pyname}
%{python2_sitelib}/%{pyname}-*.egg-info
%exclude %{python2_sitelib}/%{pyname}/tests

%files -n python2-%{sname}-tests
%license LICENSE
%{python2_sitelib}/%{pyname}/tests

%if 0%{?with_python3}
%files -n python3-%{sname}
%license LICENSE
%doc doc/source/readme.rst README.rst
%{python3_sitelib}/%{pyname}
%{python3_sitelib}/%{pyname}-*.egg-info
%exclude %{python3_sitelib}/%{pyname}/tests

%files -n python3-%{sname}-tests
%license LICENSE
%{python3_sitelib}/%{pyname}/tests

%endif # with_python3

%files -n python-%{sname}-doc
%license LICENSE
%doc doc/build/html README.rst

%changelog

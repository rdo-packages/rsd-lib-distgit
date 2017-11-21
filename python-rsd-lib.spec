%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%if 0%{?fedora} >= 24
%global with_python3 1
%endif

%global sname rsd-lib

Name:           python-%{sname}
Version:        XXX
Release:        XXX
Summary:        Python library for interfacing with Intel Rack Scale Design enabled hardware.

License:        ASL 2.0
URL:            http://git.openstack.org/cgit/openstack/%{sname}
Source0:        http://tarballs.openstack.org/%{sname}/%{sname}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python2-devel
BuildRequires:  python-jsonschema
BuildRequires:  python-oslotest >= 1.10.0
BuildRequires:  python-pbr >= 2.0
BuildRequires:  python-reno >= 1.8.0
BuildRequires:  python-setuptools
BuildRequires:  python-subunit >= 0.0.18
BuildRequires:  python-sushy >= 0.1.0
BuildRequires:  python2-sushy-tests >= 0.1.0
BuildRequires:  python-testrepository >= 0.0.18
BuildRequires:  python-testtools >= 1.4.0

Requires:       python-jsonschema
Requires:       python-pbr >= 2.0
Requires:       python-sushy >= 0.1.0

%description
This library extends the existing Sushy library to include functionality for
Intel RackScale Design enabled hardware. Capabilities include logical node
composition and decomposition, remote storage discovery and composition,
and NVMe over PCIe drive attaching and detaching to logical nodes.

%package -n     python2-%{sname}
Summary:        %{summary}
%{?python_provide:%python_provide python2-rsd-lib}

%description -n python2-%{sname}
This library extends the existing Sushy library to include functionality for
Intel RackScale Design enabled hardware. Capabilities include logical node
composition and decomposition, remote storage discovery and composition,
and NVMe over PCIe drive attaching and detaching to logical nodes.

%if 0%{?with_python3}
%package -n     python3-%{sname}
Summary:        %{summary}

BuildRequires:  python3-devel
BuildRequires:  python3-jsonschema
BuildRequires:  python3-oslotest >= 1.10.0
BuildRequires:  python3-pbr >= 2.0
BuildRequires:  python3-reno >= 1.8.0
BuildRequires:  python3-setuptools
BuildRequires:  python3-subunit >= 0.0.18
BuildRequires:  python3-sushy >= 0.1.0
BuildRequires:  python3-sushy-tests >= 0.1.0
BuildRequires:  python3-testrepository >= 0.0.18
BuildRequires:  python3-testtools >= 1.4.0

Requires:       python3-pbr >= 2.0
Requires:       python3-sushy >= 0.1.0
Requires:       python3-jsonschema

%description -n python3-%{sname}
This library extends the existing Sushy library to include functionality for
Intel RackScale Design enabled hardware. Capabilities include logical node
composition and decomposition, remote storage discovery and composition,
and NVMe over PCIe drive attaching and detaching to logical nodes.

%endif # with_python3

%prep
%autosetup -n %{sname}-%{upstream_version}

%build
%py2_build
%if 0%{?with_python3}
%py3_build
%endif

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
%{python2_sitelib}/%{sname}
%{python2_sitelib}/%{sname}-%{version}-py?.?.egg-info

%if 0%{?with_python3}
%files -n python3-%{sname}
%license LICENSE
%doc doc/source/readme.rst README.rst
%{python3_sitelib}/%{sname}
%{python3_sitelib}/%{sname}-%{version}-py?.?.egg-info
%endif # with_python3

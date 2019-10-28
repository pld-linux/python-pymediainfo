#
# Conditional build:
%bcond_with	doc	# don't build doc
%bcond_with	tests	# do not perform "make test"
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define 	module		pymediainfo
%define 	egg_name	pymediainfo
%define		pypi_name	pymediainfo
Summary:	A Python wrapper for the mediainfo library
Name:		python-%{pypi_name}
Version:	2.2.0
Release:	3
License:	MIT
Group:		Libraries/Python
Source0:	https://files.pythonhosted.org/packages/source/p/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
# Source0-md5:	66602dc7015648e7735a2abae346deea
URL:		https://github.com/sbraz/pymediainfo
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with python2}
BuildRequires:	python-devel
%if %{with tests}
BuildRequires:	python2-pytest
BuildRequires:	python2-pytest-runner
BuildRequires:	python2-setuptools
BuildRequires:	python2-sphinx
%endif
%endif
%if %{with python3}
BuildRequires:	python3-devel
%if %{with tests}
BuildRequires:	python3-pytest
BuildRequires:	python3-pytest-runner
BuildRequires:	python3-setuptools
%endif
%endif
Requires:	libmediainfo
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This small package is a wrapper around the MediaInfo library.

%package -n python3-%{pypi_name}
Summary:	A Python wrapper for the mediainfo library
Group:		Libraries/Python
Requires:	libmediainfo

%description -n python3-%{pypi_name}
This small package is a wrapper around the MediaInfo library.

%prep
%setup -q -n %{pypi_name}-%{version}

# Remove bundled egg-info
%{__rm} -r %{egg_name}.egg-info

%build
%if %{with python2}
%py_build %{?with_tests:test}

%if %{with doc}
# generate html docs
sphinx-build docs html
# remove the sphinx-build leftovers
%{__rm} -r html/.{doctrees,buildinfo}
%endif
%endif

%if %{with python3}
%py3_build %{?with_tests:test}

%if %{with doc}
# generate html docs
python3-sphinx-build docs html
# remove the sphinx-build leftovers
%{__rm} -r html/.{doctrees,buildinfo}
%endif
%endif

%install
rm -rf $RPM_BUILD_ROOT
%if %{with python2}
%py_install
%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc README.rst %{?with_doc:html}
%{py_sitescriptdir}/%{module}
%{py_sitescriptdir}/%{egg_name}-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-%{pypi_name}
%defattr(644,root,root,755)
%doc README.rst %{?with_doc:html}
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/%{egg_name}-%{version}-py*.egg-info
%endif

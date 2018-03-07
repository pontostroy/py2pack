%define          debug_package %{nil}
#
# spec file for package python-{{ name }}
#
# Copyright (c) {{ year }} {{ user_name }}.
#
%{!?python_sitelib: %global python_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:           python-{{ name }}
Version:        {{ version }}
Release:        0
Url:            {{ home_page }}
Summary:        {{ summary }}
License:        {{ license }}
Group:          Development/Languages/Python
Source:         {{ source_url|replace(version, '%{version}') }}
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildRequires:  python-devel {%- if requires_python %} = {{ requires_python }} {% endif %}
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  python-libs
{%- if setup_requires and setup_requires is not none %}
{%- for req in setup_requires|sort %}
BuildRequires:  python-{{ req|replace('(','')|replace(')','') }}
{%- endfor %}
{%- endif %}
{%- if (install_requires and install_requires is not none) or (tests_require and tests_require is not none) %}
# SECTION test requirements
{%- if install_requires and install_requires is not none %}
{%- for req in install_requires|sort %}
BuildRequires:  python-{{ req|replace('(','')|replace(')','') }}
{%- endfor %}
{%- endif %}
{%- if tests_require and tests_require is not none %}
{%- for req in tests_require|sort %}
BuildRequires:  python-{{ req|replace('(','')|replace(')','') }}
{%- endfor %}
{%- endif %}
# /SECTION
{%- endif %}
{%- if source_url.endswith('.zip') %}
BuildRequires:  unzip
{%- endif %}
BuildRequires:  fdupes
{%- if install_requires and install_requires is not none %}
{%- for req in install_requires|sort %}
Requires:       python-{{ req|replace('(','')|replace(')','') }}
{%- endfor %}
{%- endif %}
{%- if extras_require and extras_require is not none %}
{%- for reqlist in extras_require.values() %}
{%- for req in reqlist %}
Suggests:       python-{{ req|replace('(','')|replace(')','') }}
{%- endfor %}
{%- endfor %}
{%- endif %}
{%- if not has_ext_modules %}
BuildArch:      noarch
{%- endif %}
%{?python_provide:%python_provide python2-%{mod_name}}
%description
{{ description }}

%prep
%setup -q -n {{ name }}-%{version}

%build
{%- if is_extension %}
export CFLAGS="%{optflags}"
{%- endif %}
python setup.py build

%install
python setup.py install --prefix=%{_prefix} --root=%{buildroot}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
{%- if doc_files %}
%doc {{ doc_files|join(" ") }}
{%- endif %}
{%- if scripts and scripts is not none %}
{%- for script in scripts %}
%{_bindir}/{{ script|basename }}
{%- endfor %}
{%- endif %}
%{python_sitelib}/*

%changelog


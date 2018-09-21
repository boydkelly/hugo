# If any of the following macros should be set otherwise,
# you can wrap any of them with the following conditions:
# - %%if 0%%{centos} == 7
# - %%if 0%%{?rhel} == 7
# - %%if 0%%{?fedora} == 23
# Or just test for particular distribution:
# - %%if 0%%{centos}
# - %%if 0%%{?rhel}
# - %%if 0%%{?fedora}
#
# Be aware, on centos, both %%rhel and %%centos are set. If you want to test
# rhel specific macros, you can use %%if 0%%{?rhel} && 0%%{?centos} == 0 condition.
# (Don't forget to replace double percentage symbol with single one in order to apply a condition)

# Generate devel rpm
%global with_devel 1
# Build project from bundled dependencies
%global with_bundled 0
# Build with debug info rpm
%global with_debug 1
# Run tests in check section
%global with_check 1
# Generate unit-test rpm
%global with_unit_test 1

%if 0%{?with_debug}
%global _dwz_low_mem_die_limit 0
%else
%global debug_package   %{nil}
%endif

%if ! 0%{?gobuild:1}
%global gobuild(o:) go build -ldflags "${LDFLAGS:-} -B 0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \\n')" -a -v -x %{?**};
%endif

%global provider        github
%global provider_tld    com
%global project         gohugoio
%global repo            hugo
# https://github.com/gohugoio/hugo
%global provider_prefix %{provider}.%{provider_tld}/%{project}/%{repo}
%global import_path     %{provider_prefix}
# This commit is the 0.37 tag
%global commit          456f5476cf9bf96c558448372058130fee1f9330 
%global shortcommit     %(c=%{commit}; echo ${c:0:7})

Name:           hugo
Version:        0.48
Release:        0%{?dist}
Summary:        A Fast and Flexible Static Site Generator built with love in GoLang
License:        ASL 2.0 and MIT
URL:            https://%{provider_prefix}
Source0:        https://%{provider_prefix}/archive/%{commit}/%{repo}-%{version}.tar.gz

# e.g. el6 has ppc64 arch without gcc-go, so EA tag is required
ExclusiveArch:  %{?go_arches:%{go_arches}}%{!?go_arches:%{ix86} x86_64 aarch64 %{arm}}
# If go_compiler is not set to 1, there is no virtual provide. Use golang instead.
BuildRequires:  %{?go_compiler:compiler(go-compiler)}%{!?go_compiler:golang}

%if ! 0%{?with_bundled}
# main.go
BuildRequires: golang(github.com/spf13/jwalterweatherman)

# magefile.go
# No need in BRing these
# BuildRequires: golang(github.com/magefile/mage/mg)
# BuildRequires: golang(github.com/magefile/mage/sh)

# Remaining dependencies not included in main packages
BuildRequires: golang(github.com/yosssi/ace)
BuildRequires: golang(golang.org/x/text/unicode/norm)
BuildRequires: golang(github.com/alecthomas/chroma/formatters/html)
BuildRequires: golang(github.com/BurntSushi/toml)
BuildRequires: golang(github.com/hashicorp/go-immutable-radix)
BuildRequires: golang(github.com/russross/blackfriday)
BuildRequires: golang(golang.org/x/text/transform)
BuildRequires: golang(github.com/markbates/inflect)
BuildRequires: golang(gopkg.in/yaml.v2)
BuildRequires: golang(github.com/mitchellh/mapstructure)
BuildRequires: golang(github.com/spf13/viper)
BuildRequires: golang(github.com/fsnotify/fsnotify)
BuildRequires: golang(github.com/spf13/fsync)
BuildRequires: golang(github.com/alecthomas/chroma)
BuildRequires: golang(github.com/spf13/afero)
BuildRequires: golang(github.com/spf13/cast)
BuildRequires: golang(github.com/alecthomas/chroma/lexers)
BuildRequires: golang(github.com/chaseadamsio/goorgeous)
BuildRequires: golang(github.com/nicksnyder/go-i18n/i18n/bundle)
BuildRequires: golang(github.com/nicksnyder/go-i18n/i18n/language)
BuildRequires: golang(github.com/kyokomi/emoji)
BuildRequires: golang(github.com/gorilla/websocket)
BuildRequires: golang(github.com/eknkc/amber)
BuildRequires: golang(github.com/spf13/cobra/doc)
BuildRequires: golang(github.com/alecthomas/chroma/styles)
BuildRequires: golang(github.com/spf13/pflag)
BuildRequires: golang(github.com/miekg/mmark)
BuildRequires: golang(github.com/jdkato/prose/transform)
BuildRequires: golang(github.com/PuerkitoBio/purell)
BuildRequires: golang(github.com/spf13/nitro)
BuildRequires: golang(github.com/alecthomas/chroma/formatters)
BuildRequires: golang(github.com/spf13/cobra)
BuildRequires: golang(github.com/bep/gitmap)
BuildRequires: golang(golang.org/x/image/webp)
BuildRequires: golang(github.com/disintegration/imaging)
BuildRequires: golang(github.com/gobwas/glob)
BuildRequires: golang(github.com/muesli/smartcrop)
BuildRequires: golang(github.com/olekukonko/tablewriter)
BuildRequires: golang(golang.org/x/net/context)
BuildRequires: golang(golang.org/x/sync/errgroup)
%endif

%description
Hugo is a static HTML and CSS website generator written in Go. It is optimized
for speed, easy use and configurability. Hugo takes a directory with content
and templates and renders them into a full HTML website.

%if 0%{?with_devel}
%package -n golang-%{provider}-%{project}-%{repo}-devel
Summary:       %{summary}
BuildArch:     noarch

%if 0%{?with_check} && ! 0%{?with_bundled}
BuildRequires: golang(github.com/BurntSushi/toml)
BuildRequires: golang(github.com/PuerkitoBio/purell)
BuildRequires: golang(github.com/alecthomas/chroma)
BuildRequires: golang(github.com/alecthomas/chroma/formatters)
BuildRequires: golang(github.com/alecthomas/chroma/formatters/html)
BuildRequires: golang(github.com/alecthomas/chroma/lexers)
BuildRequires: golang(github.com/alecthomas/chroma/styles)
BuildRequires: golang(github.com/bep/gitmap)
BuildRequires: golang(github.com/markbates/inflect)
BuildRequires: golang(github.com/chaseadamsio/goorgeous)
BuildRequires: golang(github.com/eknkc/amber)
BuildRequires: golang(github.com/fsnotify/fsnotify)
BuildRequires: golang(github.com/gorilla/websocket)
BuildRequires: golang(github.com/hashicorp/go-immutable-radix)
BuildRequires: golang(github.com/jdkato/prose/transform)
BuildRequires: golang(github.com/kyokomi/emoji)
BuildRequires: golang(github.com/miekg/mmark)
BuildRequires: golang(github.com/mitchellh/mapstructure)
BuildRequires: golang(github.com/nicksnyder/go-i18n/i18n/bundle)
BuildRequires: golang(github.com/nicksnyder/go-i18n/i18n/language)
BuildRequires: golang(github.com/russross/blackfriday)
BuildRequires: golang(github.com/spf13/afero)
BuildRequires: golang(github.com/spf13/cast)
BuildRequires: golang(github.com/spf13/cobra)
BuildRequires: golang(github.com/spf13/cobra/doc)
BuildRequires: golang(github.com/spf13/fsync)
BuildRequires: golang(github.com/spf13/jwalterweatherman)
BuildRequires: golang(github.com/spf13/nitro)
BuildRequires: golang(github.com/spf13/pflag)
BuildRequires: golang(github.com/spf13/viper)
BuildRequires: golang(github.com/yosssi/ace)
BuildRequires: golang(golang.org/x/text/transform)
BuildRequires: golang(golang.org/x/text/unicode/norm)
BuildRequires: golang(gopkg.in/yaml.v2)
BuildRequires: golang(golang.org/x/image/webp)
BuildRequires: golang(github.com/disintegration/imaging)
BuildRequires: golang(github.com/gobwas/glob)
BuildRequires: golang(github.com/muesli/smartcrop)
BuildRequires: golang(github.com/olekukonko/tablewriter)
BuildRequires: golang(golang.org/x/net/context)
BuildRequires: golang(golang.org/x/sync/errgroup)
%endif

Requires:      golang(github.com/BurntSushi/toml)
Requires:      golang(github.com/PuerkitoBio/purell)
Requires:      golang(github.com/alecthomas/chroma)
Requires:      golang(github.com/alecthomas/chroma/formatters)
Requires:      golang(github.com/alecthomas/chroma/formatters/html)
Requires:      golang(github.com/alecthomas/chroma/lexers)
Requires:      golang(github.com/alecthomas/chroma/styles)
Requires:      golang(github.com/bep/gitmap)
Requires:      golang(github.com/markbates/inflect)
Requires:      golang(github.com/chaseadamsio/goorgeous)
Requires:      golang(github.com/eknkc/amber)
Requires:      golang(github.com/fsnotify/fsnotify)
Requires:      golang(github.com/gorilla/websocket)
Requires:      golang(github.com/hashicorp/go-immutable-radix)
Requires:      golang(github.com/jdkato/prose/transform)
Requires:      golang(github.com/kyokomi/emoji)
Requires:      golang(github.com/miekg/mmark)
Requires:      golang(github.com/mitchellh/mapstructure)
Requires:      golang(github.com/nicksnyder/go-i18n/i18n/bundle)
Requires:      golang(github.com/nicksnyder/go-i18n/i18n/language)
Requires:      golang(github.com/russross/blackfriday)
Requires:      golang(github.com/spf13/afero)
Requires:      golang(github.com/spf13/cast)
Requires:      golang(github.com/spf13/cobra)
Requires:      golang(github.com/spf13/cobra/doc)
Requires:      golang(github.com/spf13/fsync)
Requires:      golang(github.com/spf13/jwalterweatherman)
Requires:      golang(github.com/spf13/nitro)
Requires:      golang(github.com/spf13/pflag)
Requires:      golang(github.com/spf13/viper)
Requires:      golang(github.com/yosssi/ace)
Requires:      golang(golang.org/x/text/transform)
Requires:      golang(golang.org/x/text/unicode/norm)
Requires:      golang(gopkg.in/yaml.v2)
Requires:      golang(golang.org/x/image/webp)
Requires:      golang(github.com/disintegration/imaging)
Requires:      golang(github.com/gobwas/glob)
Requires:      golang(github.com/muesli/smartcrop)
Requires:      golang(github.com/olekukonko/tablewriter)
Requires:      golang(golang.org/x/net/context)
Requires:      golang(golang.org/x/sync/errgroup)

Provides:      golang(%{import_path}/bufferpool) = %{version}-%{release}
Provides:      golang(%{import_path}/cache) = %{version}-%{release}
Provides:      golang(%{import_path}/commands) = %{version}-%{release}
Provides:      golang(%{import_path}/common/types) = %{version}-%{release}
Provides:      golang(%{import_path}/compare) = %{version}-%{release}
Provides:      golang(%{import_path}/config) = %{version}-%{release}
Provides:      golang(%{import_path}/create) = %{version}-%{release}
Provides:      golang(%{import_path}/deps) = %{version}-%{release}
Provides:      golang(%{import_path}/docshelper) = %{version}-%{release}
Provides:      golang(%{import_path}/helpers) = %{version}-%{release}
Provides:      golang(%{import_path}/hugofs) = %{version}-%{release}
Provides:      golang(%{import_path}/hugolib) = %{version}-%{release}
Provides:      golang(%{import_path}/i18n) = %{version}-%{release}
Provides:      golang(%{import_path}/livereload) = %{version}-%{release}
Provides:      golang(%{import_path}/media) = %{version}-%{release}
Provides:      golang(%{import_path}/metrics) = %{version}-%{release}
Provides:      golang(%{import_path}/output) = %{version}-%{release}
Provides:      golang(%{import_path}/parser) = %{version}-%{release}
Provides:      golang(%{import_path}/related) = %{version}-%{release}
Provides:      golang(%{import_path}/releaser) = %{version}-%{release}
Provides:      golang(%{import_path}/source) = %{version}-%{release}
Provides:      golang(%{import_path}/tpl) = %{version}-%{release}
Provides:      golang(%{import_path}/tpl/cast) = %{version}-%{release}
Provides:      golang(%{import_path}/tpl/collections) = %{version}-%{release}
Provides:      golang(%{import_path}/tpl/compare) = %{version}-%{release}
Provides:      golang(%{import_path}/tpl/crypto) = %{version}-%{release}
Provides:      golang(%{import_path}/tpl/data) = %{version}-%{release}
Provides:      golang(%{import_path}/tpl/encoding) = %{version}-%{release}
Provides:      golang(%{import_path}/tpl/fmt) = %{version}-%{release}
Provides:      golang(%{import_path}/tpl/images) = %{version}-%{release}
Provides:      golang(%{import_path}/tpl/inflect) = %{version}-%{release}
Provides:      golang(%{import_path}/tpl/lang) = %{version}-%{release}
Provides:      golang(%{import_path}/tpl/math) = %{version}-%{release}
Provides:      golang(%{import_path}/tpl/os) = %{version}-%{release}
Provides:      golang(%{import_path}/tpl/partials) = %{version}-%{release}
Provides:      golang(%{import_path}/tpl/safe) = %{version}-%{release}
Provides:      golang(%{import_path}/tpl/strings) = %{version}-%{release}
Provides:      golang(%{import_path}/tpl/time) = %{version}-%{release}
Provides:      golang(%{import_path}/tpl/tplimpl) = %{version}-%{release}
Provides:      golang(%{import_path}/tpl/transform) = %{version}-%{release}
Provides:      golang(%{import_path}/tpl/urls) = %{version}-%{release}
Provides:      golang(%{import_path}/transform) = %{version}-%{release}
Provides:      golang(%{import_path}/utils) = %{version}-%{release}
Provides:      golang(%{import_path}/watcher) = %{version}-%{release}
Provides:      golang(%{import_path}/resource) = %{version}-%{release}

%description -n golang-%{provider}-%{project}-%{repo}-devel
%{summary}

This package contains library source intended for
building other packages which use import path with
%{import_path} prefix.
%endif

%if 0%{?with_unit_test} && 0%{?with_devel}
%package -n golang-%{provider}-%{project}-%{repo}-unit-test-devel
Summary:         Unit tests for %{name} package
%if 0%{?with_check}
#Here comes all BuildRequires: PACKAGE the unit tests
#in %%check section need for running
%endif

# test subpackage tests code from devel subpackage
Requires:        golang-%{provider}-%{project}-%{repo}-devel = %{version}-%{release}

%if 0%{?with_check} && ! 0%{?with_bundled}
BuildRequires: golang(github.com/fortytw2/leaktest)
BuildRequires: golang(github.com/stretchr/testify/assert)
BuildRequires: golang(github.com/stretchr/testify/require)
%endif

Requires:      golang(github.com/fortytw2/leaktest)
Requires:      golang(github.com/stretchr/testify/assert)
Requires:      golang(github.com/stretchr/testify/require)

# These are used during hugolib tests
%%if 0%{?with_check}
BuildRequires: python3-docutils
BuildRequires: python3-pygments
BuildRequires: rubygem-asciidoctor
Requires:      python3-docutils
Requires:      python3-pygments
Requires:      rubygem-asciidoctor
%%endif

%description -n golang-%{provider}-%{project}-%{repo}-unit-test-devel
%{summary}

This package contains unit tests for project
providing packages with %{import_path} prefix.
%endif

%prep
%setup -q -n %{repo}-%{commit}

%build
mkdir -p src/%{provider}.%{provider_tld}/%{project}
ln -s ../../../ src/%{import_path}

%if ! 0%{?with_bundled}
export GOPATH=$(pwd):%{gopath}
%else
# No dependency directories so far
export GOPATH=$(pwd):%{gopath}
%endif

%gobuild -o bin/hugo %{import_path}/

%install
install -d -p %{buildroot}%{_bindir}
install -p -m 0755 bin/hugo %{buildroot}%{_bindir}

# source codes for building projects
%if 0%{?with_devel}
install -d -p %{buildroot}/%{gopath}/src/%{import_path}/
echo "%%dir %%{gopath}/src/%%{import_path}/." >> devel.file-list
# find all *.go but no *_test.go files and generate devel.file-list
for file in $(find . \( -iname "*.go" -or -iname "*.s" \) \! -iname "*_test.go") ; do
    dirprefix=$(dirname $file)
    install -d -p %{buildroot}/%{gopath}/src/%{import_path}/$dirprefix
    cp -pav $file %{buildroot}/%{gopath}/src/%{import_path}/$file
    echo "%%{gopath}/src/%%{import_path}/$file" >> devel.file-list

    while [ "$dirprefix" != "." ]; do
        echo "%%dir %%{gopath}/src/%%{import_path}/$dirprefix" >> devel.file-list
        dirprefix=$(dirname $dirprefix)
    done
done
%endif

# testing files for this project
%if 0%{?with_unit_test} && 0%{?with_devel}
install -d -p %{buildroot}/%{gopath}/src/%{import_path}/
# find all *_test.go files and generate unit-test-devel.file-list
for file in $(find . -iname "*_test.go") ; do
    dirprefix=$(dirname $file)
    install -d -p %{buildroot}/%{gopath}/src/%{import_path}/$dirprefix
    cp -pav $file %{buildroot}/%{gopath}/src/%{import_path}/$file
    echo "%%{gopath}/src/%%{import_path}/$file" >> unit-test-devel.file-list

    while [ "$dirprefix" != "." ]; do
        echo "%%dir %%{gopath}/src/%%{import_path}/$dirprefix" >> devel.file-list
        dirprefix=$(dirname $dirprefix)
    done
done
# install data used for tests
cp -pav ./hugolib/testdata %{buildroot}/%{gopath}/src/%{import_path}/hugolib/
echo "%%{gopath}/src/%%{import_path}/hugolib/testdata" >> unit-test-devel.file-list
cp -pav ./resource/testdata %{buildroot}/%{gopath}/src/%{import_path}/resource/
echo "%%{gopath}/src/%%{import_path}/resource/testdata" >> unit-test-devel.file-list

%endif

%if 0%{?with_devel}
sort -u -o devel.file-list devel.file-list
%endif

%check
%if 0%{?with_check} && 0%{?with_unit_test} && 0%{?with_devel}
%if ! 0%{?with_bundled}
export GOPATH=%{buildroot}/%{gopath}:%{gopath}
%else
# No dependency directories so far

export GOPATH=%{buildroot}/%{gopath}:%{gopath}
%endif

%if ! 0%{?gotest:1}
%global gotest go test
%endif

%gotest %{import_path}/bufferpool
%gotest %{import_path}/cache
%gotest %{import_path}/commands
%gotest %{import_path}/common/types
%gotest %{import_path}/create
%gotest %{import_path}/helpers
%gotest %{import_path}/hugofs
%gotest %{import_path}/hugolib
%gotest %{import_path}/i18n
%gotest %{import_path}/media
%gotest %{import_path}/metrics
%gotest %{import_path}/output
%gotest %{import_path}/parser
%gotest %{import_path}/related
# We do not want to test upstream release process (needs git repo)
# %%gotest %%{import_path}/releaser
%gotest %{import_path}/source
%gotest %{import_path}/tpl/cast
%gotest %{import_path}/tpl/collections
%gotest %{import_path}/tpl/compare
%gotest %{import_path}/tpl/crypto
%gotest %{import_path}/tpl/data
%gotest %{import_path}/tpl/encoding
%gotest %{import_path}/tpl/fmt
%gotest %{import_path}/tpl/images
%gotest %{import_path}/tpl/inflect
%gotest %{import_path}/tpl/internal
%gotest %{import_path}/tpl/lang
%gotest %{import_path}/tpl/math
%gotest %{import_path}/tpl/os
%gotest %{import_path}/tpl/partials
%gotest %{import_path}/tpl/safe
%gotest %{import_path}/tpl/strings
# A test depends on the host timezone, we do now want to test it.
# time_test.go:49: [3] DateFormat failed: Unable to Cast 1421733600 to Time # line 35 returns different results
# %%gotest %%{import_path}/tpl/time
%gotest %{import_path}/tpl/tplimpl
%gotest %{import_path}/tpl/transform
%gotest %{import_path}/tpl/urls
%gotest %{import_path}/transform
%gotest %{import_path}/resource
%endif

#define license tag if not already defined
%{!?_licensedir:%global license %doc}

%files
%license LICENSE.md
%doc CONTRIBUTING.md README.md
%{_bindir}/hugo

%if 0%{?with_devel}
%files -n golang-%{provider}-%{project}-%{repo}-devel -f devel.file-list
%license LICENSE.md
%doc CONTRIBUTING.md README.md
%dir %{gopath}/src/%{provider}.%{provider_tld}/%{project}
%endif

%if 0%{?with_unit_test} && 0%{?with_devel}
%files -n golang-%{provider}-%{project}-%{repo}-unit-test-devel -f unit-test-devel.file-list
%license LICENSE.md
%doc CONTRIBUTING.md README.md
%endif

%changelog
* Fri Sep 21 2018 Boyd Kelly <bkelly@coastsystems.net> - 0.48
- Update version

* Thu Mar 08 2018 Athos Ribeiro <athoscr@fedoraproject.org> - 0.37.1-1
- Update version

* Thu Mar 01 2018 Athos Ribeiro <athoscr@fedoraproject.org> - 0.37-1
- Update version

* Wed Feb 21 2018 Athos Ribeiro <athoscr@fedoraproject.org> - 0.36.1-2
- Include resource/testdata in unit tests package

* Fri Feb 16 2018 Athos Ribeiro <athoscr@fedoraproject.org> - 0.36.1-1
- Update version

* Tue Feb 13 2018 Athos Ribeiro <athoscr@fedoraproject.org> - 0.36-1
- Update version

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.31.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Dec 11 2017 Pierre-Alain TORET <pierre-alain.toret@protonmail.com> - 0.31.1-1
- Update Version

* Mon Nov 20 2017 Athos Ribeiro <athoscr@fedoraproject.org> - 0.31-1
- Update Version

* Sat Oct 21 2017 Athos Ribeiro <athoscr@fedoraproject.org> - 0.30.2-1
- Update Version

* Tue Oct 17 2017 Athos Ribeiro <athoscr@fedoraproject.org> - 0.30-1
- Update Version

* Wed Oct 11 2017 Athos Ribeiro <athoscr@fedoraproject.org> - 0.29-1
- Update Version

* Fri Sep 15 2017 Athos Ribeiro <athoscr@fedoraproject.org> - 0.27.1-2
- Add MIT License

* Wed Sep 13 2017 Athos Ribeiro <athoscr@fedoraproject.org> - 0.27.1-1
- Update version

* Tue Sep 12 2017 Athos Ribeiro <athoscr@fedoraproject.org> - 0.27-1
- Update version

* Fri Aug 11 2017 Athos Ribeiro <athoscr@fedoraproject.org> - 0.26-2
- Substitute bep/inflect for markbates/inflect

* Fri Aug 11 2017 Athos Ribeiro <athoscr@fedoraproject.org> - 0.26-1
- Update version

* Mon Jul 31 2017 Athos Ribeiro <athoscr@fedoraproject.org> - 0.25.1-1
- Update version
- Fix unit-test subpackage requires to correct devel package
- Use global instead of define for gobuild

* Mon Jun 26 2017 Athos Ribeiro <athoscr@fedoraproject.org> - 0.24-2
- Add external test dependencies

* Fri Jun 23 2017 Athos Ribeiro <athoscr@fedoraproject.org> - 0.24-1
- New version
- Regenerate specfile with gofed

* Fri Mar 17 2017 Athos Ribeiro <athoscr@fedoraproject.org> - 0.19-4
- Remove empty conditionals

* Sun Mar 12 2017 Athos Ribeiro <athoscr@fedoraproject.org> - 0.19-3
- Use dist tag

* Fri Mar 03 2017 Athos Ribeiro <athoscr@fedoraproject.org> - 0.19-2
- Move test data to unit-test subpackage path

* Fri Mar 03 2017 Athos Ribeiro <athoscr@fedoraproject.org> - 0.19-1
- New version

* Fri Mar 03 2017 Athos Ribeiro <athoscr@fedoraproject.org> - 0.18.1-5
- Include testdata in unit-test-devel subpackage

* Wed Mar 01 2017 Athos Ribeiro <athoscr@fedoraproject.org> - 0.18.1-4
- Change binary name

* Wed Mar 01 2017 Athos Ribeiro <athoscr@fedoraproject.org> - 0.18.1-3
- Use lowercase for jww package

* Tue Feb 28 2017 Athos Ribeiro <athoscr@fedoraproject.org> - 0.18.1-2
- Use cammelcase for jww package

* Sun Feb 26 2017 Athos Ribeiro <athoscr@fedoraproject.org> - 0.18.1-1
- Initial package


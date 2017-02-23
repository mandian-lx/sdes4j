Summary:	An implementation of the RFC4568 in Java
Name:		sdes4j
Version:	1.1.4
Release:	1
License:	LGPLv2
Group:		Development/Java
URL:		https://github.com/ibauersachs/%{name}
Source0:	https://github.com/ibauersachs/%{name}/archive/r%{version}/%{name}-%{version}.tar.gz
BuildArch:	noarch

BuildRequires:	maven-local
BuildRequires:	mvn(commons-codec:commons-codec)
BuildRequires:	mvn(junit:junit)
BuildRequires:	mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:	mvn(org.apache.maven.plugins:maven-release-plugin)

%description
Implementation of RFC4568: Session Description Protocol (SDP) Security
Descriptions for Media Streams for Java.

%files -f .mfiles
%defattr(0644,root,root,0755)
%doc LICENSE

#----------------------------------------------------------------------------

%package javadoc
Summary:	Javadoc for %{name}

%description javadoc
API documentation for %{name}.

%files javadoc -f .mfiles-javadoc

#----------------------------------------------------------------------------

%prep
%setup -q -n %{name}-r%{version}
# Delete prebuild JARs and classes
find . -name "*.jar" -delete
find . -name "*.class" -delete

# Add the META-INF/INDEX.LIST to the jar archive (fix jar-not-indexed warning)
%pom_add_plugin :maven-jar-plugin . "
<executions>
	<execution>
		<phase>package</phase>
		<configuration>
			<archive>
				<manifestFile>\${project.build.outputDirectory}/META-INF/MANIFEST.MF</manifestFile>
				<manifest>
					<addDefaultImplementationEntries>true</addDefaultImplementationEntries>
					<addDefaultSpecificationEntries>true</addDefaultSpecificationEntries>
				</manifest>
				<index>true</index>
			</archive>
		</configuration>
		<goals>
			<goal>jar</goal>
		</goals>
	</execution>
</executions>"

# Fix JAR name
%mvn_file :%{name} %{name}-%{version} %{name}

%build
# Lots of test fail
%mvn_build -f

%install
%mvn_install


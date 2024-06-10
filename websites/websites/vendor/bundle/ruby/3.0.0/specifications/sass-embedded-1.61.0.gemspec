# -*- encoding: utf-8 -*-
# stub: sass-embedded 1.61.0 ruby lib
# stub: ext/sass/Rakefile

Gem::Specification.new do |s|
  s.name = "sass-embedded".freeze
  s.version = "1.61.0"

  s.required_rubygems_version = Gem::Requirement.new(">= 0".freeze) if s.respond_to? :required_rubygems_version=
  s.metadata = { "documentation_uri" => "https://rubydoc.info/gems/sass-embedded/1.61.0", "funding_uri" => "https://github.com/sponsors/ntkme", "source_code_uri" => "https://github.com/ntkme/sass-embedded-host-ruby/tree/v1.61.0" } if s.respond_to? :metadata=
  s.require_paths = ["lib".freeze]
  s.authors = ["\u306A\u3064\u304D".freeze]
  s.date = "2023-04-06"
  s.description = "A Ruby library that will communicate with Embedded Dart Sass using the Embedded Sass protocol.".freeze
  s.email = ["i@ntk.me".freeze]
  s.extensions = ["ext/sass/Rakefile".freeze]
  s.files = ["ext/sass/Rakefile".freeze]
  s.homepage = "https://github.com/ntkme/sass-embedded-host-ruby".freeze
  s.licenses = ["MIT".freeze]
  s.required_ruby_version = Gem::Requirement.new(">= 2.7.0".freeze)
  s.rubygems_version = "3.3.5".freeze
  s.summary = "Use dart-sass with Ruby!".freeze

  s.installed_by_version = "3.3.5" if s.respond_to? :installed_by_version

  if s.respond_to? :specification_version then
    s.specification_version = 4
  end

  if s.respond_to? :add_runtime_dependency then
    s.add_runtime_dependency(%q<google-protobuf>.freeze, ["~> 3.21"])
    s.add_runtime_dependency(%q<rake>.freeze, [">= 10.0.0"])
    s.add_development_dependency(%q<rspec>.freeze, ["~> 3.12.0"])
    s.add_development_dependency(%q<rubocop>.freeze, ["~> 1.49.0"])
    s.add_development_dependency(%q<rubocop-performance>.freeze, ["~> 1.16.0"])
    s.add_development_dependency(%q<rubocop-rake>.freeze, ["~> 0.6.0"])
    s.add_development_dependency(%q<rubocop-rspec>.freeze, ["~> 2.19.0"])
  else
    s.add_dependency(%q<google-protobuf>.freeze, ["~> 3.21"])
    s.add_dependency(%q<rake>.freeze, [">= 10.0.0"])
    s.add_dependency(%q<rspec>.freeze, ["~> 3.12.0"])
    s.add_dependency(%q<rubocop>.freeze, ["~> 1.49.0"])
    s.add_dependency(%q<rubocop-performance>.freeze, ["~> 1.16.0"])
    s.add_dependency(%q<rubocop-rake>.freeze, ["~> 0.6.0"])
    s.add_dependency(%q<rubocop-rspec>.freeze, ["~> 2.19.0"])
  end
end

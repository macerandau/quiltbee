Pod::Spec.new do |s|
  s.name = 'QuiltbeeNative'
  s.version = '1.0.0'
  s.summary = 'Quilt Bee keychain counter and PDF share sheet'
  s.license = 'UNLICENSED'
  s.homepage = 'https://quiltbee.app'
  s.author = 'Quilt Bee'
  s.source = { :git => 'https://github.com/macerandau/quiltbee.git', :tag => s.version.to_s }
  s.source_files = 'ios/Sources/**/*.swift'
  s.ios.deployment_target = '13.0'
  s.dependency 'Capacitor'
  s.swift_version = '5.1'
end

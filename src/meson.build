pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
moduledir = join_paths(pkgdatadir, 'shoppinglist')
gnome = import('gnome')

gnome.compile_resources('shoppinglist',
  'shoppinglist.gresource.xml',
  gresource_bundle: true,
  install: true,
  install_dir: pkgdatadir,
)

python3 = import('python3')

conf = configuration_data()
conf.set('PYTHON', python3.find_python().path())
conf.set('VERSION', meson.project_version())
conf.set('localedir', join_paths(get_option('prefix'), get_option('localedir')))
conf.set('pkgdatadir', pkgdatadir)

configure_file(
  input: 'shoppinglist.in',
  output: 'shoppinglist',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir')
)

shoppinglist_sources = [
  '__init__.py',
  'gi_composites.py',
  'main.py',
  'window.py',
]

install_data(shoppinglist_sources, install_dir: moduledir)

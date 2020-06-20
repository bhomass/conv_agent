from setuptools import setup, find_packages
from functools import reduce

long_description = """Covid 19 answering agent."""

version = '0.1.0'

with open("covid19_agent/version.py", 'w') as f:
    f.write('# generated by setup.py\nversion = "{}"\n'.format(version))

extras = {
    'notebooks': ['jupyter', 'tqdm']
}
#extras['tests'] = reduce(lambda l1, l2: l1+l2, extras.values(), ['pytest>=3.5'])
#extras['docs'] = ['sphinx', 'sphinx_rtd_theme']
3extras['all'] = list(reduce(lambda s, l: s.union(l), extras.values(), set()))

setup(name='covid19-agent',
      version=version,
      description='Covid 19 answering agent',
      author='covid19 answer agent developer',
      author_email='bhomass@gmail.com',
      url='https://github.com/bhomass/covid19_agent.git',
      long_description=long_description,
      long_description_content_type='text/markdown',
      license='Apache License 2.0',
      packages=[pkg for pkg in find_packages() if pkg.startswith('aif360')],
      python_requires='>=3.5',
      install_requires=[
          'allennlp>=1.0.0',
          'allennlp-models>=1.0.0'
      ],
      extras_require=extras,
      #package_data={'aif360': ['data/*', 'data/*/*', 'data/*/*/*']},
      include_package_data=False,
      zip_safe=False)
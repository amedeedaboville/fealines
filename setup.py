from setuptools import setup

setup(
        name = "fealines",
        version = "0.1",
        author = "Amédée d'Aboville",
        author_email = "amedee.daboville@gmail.com",
        description = ("A PyQt application to visualize interaxon Muse data and perform biofeedback."),
        license = "BSD",
        keywords = "pyqt4 eeg muse",
        packages=['src', 'tests'],
        install_requires=[
            'PyQt4',
            'pyqtgraph'
            ],
        classifiers=[
            "Development Status :: 3 - Alpha",
            ],
        )

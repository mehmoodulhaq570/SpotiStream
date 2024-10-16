from setuptools import setup, find_packages

# Read the README file for long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="spoti_stream",  # Name of the package
    version="0.1.0",  # Version of the package
    author="Mehmood Ul Haq",  # Your name as the author
    author_email="mehmoodulhaq1040@gmail.com",  # Your email
    description="A tool to download Spotify playlist songs using YouTube",  # Short description
    long_description=long_description,  # Long description from README
    long_description_content_type="text/markdown",  # Format of the README file
    url="https://github.com/mehmoodulhaq570/SpotiStream",  # URL to the project
    project_urls={
        "Documentation": "https://github.com/mehmoodulhaq570/SpotiStream#readme",
        "Source": "https://github.com/mehmoodulhaq570/SpotiStream",
        "Bug Tracker": "https://github.com/mehmoodulhaq570/SpotiStream/issues",
    },
    packages=find_packages(),  # Automatically find all packages in the directory
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # Minimum version of Python required
    install_requires=[  # List of dependencies for the package
        "spotipy>=2.19.0",
        "yt-dlp>=2021.12.1",
        "moviepy>=1.0.3",
        "pydub>=0.25.1",  # Optional, if used
    ],
    entry_points={  # Entry points to create command-line tools
        'console_scripts': [
            'spoti_fly=spoti_stream.main:main',  # Creates a CLI command 'spoti_fly'
        ],
    },
    include_package_data=True,  # Include additional files specified in MANIFEST.in
    license="MIT",  # License for your package
)

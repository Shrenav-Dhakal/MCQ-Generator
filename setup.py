from setuptools import find_packages,setup

setup(
    name = 'mcqgenerator',
    version='0.0.1',
    author='Shrenav-Dhakal',
    author_email="dshrenav123456@gmail.com",
    install_requires = ['langchain_google_genai', 'langchain', 'streamlit', 'python-dotenv', 'PyPDF2'],
    packages = find_packages()
)
#installing local packages

from setuptools import find_packages,setup
setup(
    name='mcq_generator',
    version='0.0.1',
    author='Ganesh reddy',
    author_email='b.ganesh.reddy.05@gmail.com',
    install_requires=["langchain_openai","langchain","python-dotenv","streamlit","PyPDF2"],
    packages=find_packages()
)
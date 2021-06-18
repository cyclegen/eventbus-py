import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="eventbus-py",
    version="0.0.1",
    author="CycleGen",
    author_email="pypi@cyclegen.cloud",
    description="An eventbus that used for FinanGen",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cyclegen/eventbus-py",
    project_urls={
        "Bug Tracker": "https://github.com/cyclegen/eventbus-py/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Natural Language :: Chinese (Simplified)",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
# setup(
#     name='eventbus',
#     version='v0.1.0',
#     description='An eventbus that used for FinanGen', # 简要描述
#     py_modules=['eventbus'],   #  需要打包的模块
#     author='CycleGen', # 作者名
#     author_email='me@cyclegen.cloud',   # 作者邮件
#     url='https://github.com/cyclegen/eventbus-py', # 项目地址,一般是代码托管的网站
#     # requires=['requests','urllib3'], # 依赖包,如果没有,可以不要
#     license='MIT'
# )
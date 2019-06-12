FROM python:3.6-stretch

# Add requirements file used by pip install
ADD ./requirements.txt /predict-python/
WORKDIR /predict-python

# Run pip install to install all python dependenies
RUN pip3 install --no-cache-dir -r requirements.txt && \
    pip3 install --no-cache-dir git+git://github.com/scikit-multiflow/scikit-multiflow.git#egg=scikit-multiflow

# Add all the project files
ADD . /predict-python

EXPOSE 8000

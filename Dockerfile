# Choose our version of Python
FROM python:3.10.13

EXPOSE 8501
CMD mkdir -p /app

# Set up a working directory
WORKDIR app

# Copy the requirements file
COPY requirements.txt ./requirements.txt

# Install the Requirements File
RUN pip3 install -r requirements.txt

# Copy the code and other files into the working directory
COPY . .

# Define the Entry Point
ENTRYPOINT [ "streamlit","run" ]
CMD ["app.py"]
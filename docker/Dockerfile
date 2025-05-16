# Use the official Ubuntu 22.04 as the base image
FROM ubuntu:22.04

# Set environment variables to avoid interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Update the package list and install prerequisites
RUN apt-get update && \
    apt-get install -y software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update

# Install Python 3.11 and pip
RUN apt-get install -y python3.11 python3.11-venv python3.11-dev python3-pip

# Set Python 3.11 as the default python3
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1

# Install tkinter
RUN apt-get install python3-tk

# Install GCC and G++ with C++17 support
RUN apt-get install -y gcc-9 g++-9

# Set GCC and G++ to the installed version
RUN update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-9 1 && \
    update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-9 1

# Install Ninja build system
RUN apt-get install -y ninja-build

# Remove existing git packages and install required dependencies
RUN apt-get remove -y git git-core && \
    apt-get install -y libcurl4-openssl-dev && \
    apt-get install -y git

# Verify the installation
RUN python3 --version && pip3 --version && gcc --version && g++ --version && git --version && ninja --version

# Set the working directory
WORKDIR /app

# Copy the requirements.txt file into the container at /app
COPY requirements.txt /app

# # Copy the rest of the application code into the container at /app
# COPY ../ /app

# Install any needed packages specified in requirements.txt
RUN pip3 install --no-cache-dir -r /app/requirements.txt

# # Make port 80 available to the world outside this container
# EXPOSE 80

# # Define environment variable
# ENV NAME World

# # Run app.py when the container launches
# CMD ["python3", "app.py"]
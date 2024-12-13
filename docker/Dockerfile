FROM ubuntu:22.04 AS build

RUN apt-get update
RUN apt-get install

# Copy the current directory contents into the container at /usr/src/app
COPY . /tmp/ruckig

# Set the working directory in the container
WORKDIR /tmp/ruckig

# Install Python and C++ dependencies
RUN apt-get update -y && apt-get install -y --no-install-recommends \
    #g++
    build-essential \
    # gdb and valgrind
    gdb valgrind \
    # General build
    cmake git \
    #
    python3-pip \
    # tidy up
    && apt-get -y clean all

# Upgrade pip and install Python packages
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install matplotlib pandas pybind11
#RUN python3 -m pip install ruckig

# Ensure the user has permissions and clean up build directory
RUN mkdir -p /home/$USERNAME/.gnupg && chown -R $USERNAME:$USERNAME /home/$USERNAME/.gnupg
RUN chown -R $USERNAME:$USERNAME /tmp/ruckig
RUN rm -rf /tmp/ruckig/build/*

USER $USERNAME

# Install C++ dependencies
RUN mkdir -p build && cd build && \
    cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_INTERPROCEDURAL_OPTIMIZATION=ON .. &&\
    make

#     WORKDIR /tmp/ruckig

# # Command to run your Python script
# CMD ["python3", "./examples/14_tracking.py"]

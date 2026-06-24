FROM ubuntu:22.04

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3-pip \
    python3-venv \
    fastqc \
    bwa \
    samtools \
    bcftools \
    tabix \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY . /app

# Create virtual environment
RUN python3 -m venv /app/venv
ENV PATH="/app/venv/bin:$PATH"

# Install Python dependencies
RUN pip install --upgrade pip setuptools wheel
RUN pip install -e .
RUN pip install -r requirements.txt

# Create data and results directories
RUN mkdir -p /app/data /app/results

# Set entrypoint
ENTRYPOINT ["ngs-pipeline"]
CMD ["run", "--help"]

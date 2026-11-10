FROM debian:bookworm-slim

# Instalar Java 17, Python 3 y OpenSSH Server
RUN apt-get update && apt-get install -y \
    openjdk-17-jdk \
    python3 \
    python3-pip \
    openssh-server \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Instalar Hadoop 3.3.6
ENV HADOOP_VERSION=3.3.6
RUN curl -sL https://archive.apache.org/dist/hadoop/common/hadoop-${HADOOP_VERSION}/hadoop-${HADOOP_VERSION}.tar.gz | tar -xz -C /opt/ \
    && mv /opt/hadoop-${HADOOP_VERSION} /opt/hadoop

# Variables de entorno requeridas
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV HADOOP_HOME=/opt/hadoop
ENV PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin

# Configurar SSH sin contraseña para localhost y entre contenedores
RUN ssh-keygen -t rsa -P '' -f /root/.ssh/id_rsa \
    && cat /root/.ssh/id_rsa.pub >> /root/.ssh/authorized_keys \
    && chmod 600 /root/.ssh/authorized_keys

EXPOSE 22
CMD service ssh start && tail -f /dev/null
FROM nvidia/cuda:12.5.1-runtime-ubuntu22.04
ENV DEBIAN_FRONTEND=noninteractive

# 必要なパッケージのインストール
# /appはアプリのディレクトリ、/opt/artifactはアウトプット先のディレクトリ
RUN apt-get update && \
    apt-get install -y \
        git \
        python3 \
        python3-pip \
      && \
    mkdir /app /opt/artifact && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt runner.py .
# 依存ライブラリのインストール
RUN pip install -r requirements.txt

# Dockerコンテナー起動時に実行するスクリプト（後で作成）
COPY docker-entrypoint.sh /
# 実行権限を付与
RUN chmod +x /docker-entrypoint.sh /

WORKDIR /
# Dockerコンテナー起動時に実行するスクリプトを指定して実行
CMD ["/bin/bash", "/docker-entrypoint.sh"]

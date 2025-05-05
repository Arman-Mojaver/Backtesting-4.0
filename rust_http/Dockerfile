FROM rust:1.81 AS fetcher
WORKDIR /app

COPY Cargo.toml Cargo.lock ./
RUN mkdir src && echo "fn main() {}" > src/main.rs
RUN cargo fetch


FROM rust:1.81 AS builder
WORKDIR /app

COPY --from=fetcher /usr/local/cargo /usr/local/cargo
COPY . .
RUN cargo build             && \
    cargo build --release    && \
    cargo install cargo-watch --root /usr/local


FROM rust:1.81
RUN apt-get update && apt-get install -y \
      ca-certificates \
      build-essential \
    && rm -rf /var/lib/apt/lists/*


COPY --from=builder /usr/local/cargo /usr/local/cargo
COPY --from=builder /usr/local/bin/cargo-watch /usr/local/bin/cargo-watch
COPY --from=builder /app/target /app/target

WORKDIR /usr/src/app

CMD ["cargo", "watch", "-x", "run"]

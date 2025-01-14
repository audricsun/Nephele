FROM python:3.12-slim

WORKDIR /opt/nephele
RUN pip install --no-cache \
    -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple \
    uv

COPY pyproject.toml uv.lock /opt/nephele/
RUN uv sync --frozen -v

COPY manage.py .
COPY Makefile .
COPY nephele .
COPY apps .

CMD [ "uv", "run", "--","manage.py","runserver" ]
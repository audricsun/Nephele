FROM python:3.13-slim

RUN pip install -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple uv
WORKDIR /ops/nephele

COPY pyproject.toml uv.lock /ops/nephele/
RUN uv sync --frozen

COPY . .

CMD [ "uv", "run", "python","manage.py","runserver" ]
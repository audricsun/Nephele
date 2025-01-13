FROM python:3.12-slim

RUN pip install -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple uv
WORKDIR /ops/nephele

COPY pyproject.toml uv.lock /ops/nephele/
RUN uv sync --frozen -v

COPY . .

CMD [ "uv", "run", "--","manage.py","runserver" ]
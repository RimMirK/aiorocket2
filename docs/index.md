# aiorocket2

<div class="hero">
  <div>
    <p class="lead">Asynchronous Python client for the xRocket Pay API. The docs are generated directly from the package docstrings, so the reference stays close to the code and easy to maintain.</p>
    <p><a class="md-button md-button--primary" href="api/client/">Explore the API</a>
    <a class="md-button" href="examples/">See examples</a></p>
  </div>
  <div class="card">
    <h3>Quick start</h3>
    <pre class="code-block"><code>import asyncio
from aiorocket2 import xRocketClient

async def main():
    client = xRocketClient(api_key="YOUR_API_KEY")
    info = await client.get_info()
    print(info)

asyncio.run(main())</code></pre>
  </div>
</div>

<div class="card-grid">
  <div class="card">
    <h3>Async-first</h3>
    <p>Built around <code>asyncio</code> with a simple client interface.</p>
  </div>
  <div class="card">
    <h3>Typed models</h3>
    <p>Clear data models, enums and error handling are documented alongside the code.</p>
  </div>
  <div class="card">
    <h3>Auto-generated docs</h3>
    <p>Every API page is rendered from the source docstrings and published automatically.</p>
  </div>
</div>

## API reference

Browse the generated reference by area:

- [Client API](api/client.md)
- [Models](api/models.md)
- [Enums](api/enums.md)
- [Exceptions](api/exceptions.md)
- [Utilities](api/utils.md)
- [Tags](api/tags.md)

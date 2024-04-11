# Llmint
Fast, adaptive, modular data integration toolchain powered by LLM.

Configure your OpenAI key in `~/.llmint/config.yaml` as `openai_api_key: YOUR KEY`.

Given data from a data provider (source) and a data consumer (target):
```yaml
source: { "status": "on", "luminosity": 90 }
target: { "power": "active", "brightness": 0.9 }
```
We want to generate dataflow operators that convert data from the source schema to the target schema, e.g., in [Zed](https://github.com/brimdata/zed) dataflow:

```shell
rename power := status | rename brightness := luminosity | switch power ( case "on" => power := "active" case "off" => power := "inactive") | brightness := brightness / 100.0
```

..given the information about the data source and the target.

> TBD We assume the following *minimum* pieces of information are available at the data source and the target: at least one sample data record from each. The data record should contain at least partial schema information (e.g. a data record in json). 
>
> Note: unlike what's in the above example, the data records from the source and target may not correspond to the same entity and may be semantically different.
>
> Llmint will leverage any additional information to improve the accuracy of mint whenever possible. Commonly available information at data source and target: (i) Description about the data source (e.g. "smart light " for the above example); (ii) Schema information (e.g., data type, default values, required or optional, data ranges, description about each field); (iii) Additional data samples.
>
> Note that llmint is designed to handle cases where maintaining the additional information about the data sources are tedious. 

We refer to this process as *mint*.  A mint operation consists of the following stages.

**Extraction.** This stage extracts the schemas from the data source and consumer and represent them in a mint intermediate representation (MR). It allows the mint process to handle a diverse set of data sources (e.g., json files, data lakes, databases, API endpoints) while passing on a unified schema format to the next stages._

**Identification.** Given the source and target MRs this stage (i) preprocesses them to generate normalized MRs which are invariant to field ordering, capitalization etc; (ii) decides whether the source-target schema pair has been seen before. If so, skip the following steps and return any cached correspondences or mappings.

**Mapping.** Given each correspondence, this step generates a language-neutral transformation between the values and can be seen as a row of a match-action table. 

**Assembly.** Generates dataflow that coverts fields from source schema to the target schema, given the correspondences. The dataflow language can be specified by the user.

Llmint exposes the high-level modules with a declarative interface.

```python
import llmint
mint = llmint.new_mint()
```

## FAQ

> Why not dump all data to LLM and let it generate results?

Structured queries over time series data can be done more efficiently (fast and less costs) with dataflow engines. 

> Data integration is hard. How does LLM help solve the problem?

Here are a few intuitions on why the approach works for some domains. In IoT, for example, here are a few characteristics. (i) Simple schemas. In IoT, for example, the data source generates continuous stream of data records. (ii) Large volume of data. (iii) Description of the data source.

# Llmint
Fast, adaptive, modular data integration toolchain powered by LLM.

Configure your OpenAI key in ~/.chatz/config.yaml as `openai_api_key: YOUR KEY`.

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

**S1: Discovery.** Identifying the data sources that are relevant to a data consumer based on the *intent* at the data consumer and the data source's *metadata* such as text description. This stage helps scope down the semantics of the desired schema and can be seen as a pre-filtering step. Data consumer can also use this step to select known data sources.

**S2: Extraction.** This stage extracts the schemas from the data source and consumer and represent them in a mint intermediate representation (MR). It allows the mint process to handle a diverse set of data sources (e.g., json files, data lakes, databases, API endpoints) while passing on a unified schema format to the next stages.

**S3: Identification.** Given the source and target MRs this stage (i) preprocesses them to generate normalized MRs which are invariant to field ordering, capitalization etc; (ii) decides whether the source-target schema pair has been seen before. If so, skip the following steps and return any cached correspondences or mappings.

**S4: Matching.** Find the correspondences between fields in the schemas. This step generates the correspondence between fields. The process also decides whether the schemas are semantically equivalent and/or having semantically equivalent fields, depending on the pre-filtering policy.

**S5: Mapping.** Given each correspondence, this step generates a language-neutral transformation between the values and can be seen as a row of a match-action table. 

**S6: Assembly.** Generates dataflow that coverts fields from source schema to the target schema, given the correspondences. The dataflow language can be specified by the user.

S1-S3 are referred to as the frontend which extracts source schema from desired data sources. S4-S6 are referred to as the backend.  The mapping dataflow can be installed on the data pipeline or used in a query. 

The key piece of design of limit is that each step will leverage as much as data from the data source and the other steps as possible. For example, the mapping stage will not only reuse the correspondences from the matching stage, but it will also look at the source data when it is available.

> TBD We use a technique called *retrospection* which we asks the LLM to go through the generated correspondence to check each field for correctness and tracks any mistakes that we'll use for prompting in the future or rerun the generation at hand. We build this separate module as *retrospect* which can be attached to either of the stages, not only the matching stage.

## Design

Llmint focuses on three objectives: accuracy, performance, and cost.

> JIT data ingestion: A data processing pipeline typically ingests data from predefined data sources only. This limits the types of data it can ingest (i.e., a schema or a set of schemas), because the dataflow operators typically can perform over known fields. Instead, we want the data pipeline to be able to handle more data that are semantically equivalent but with different schemas. This means we want to dynamically adapt the pipeline (i.e., its ingestion component) based on the data source schema.
>
> Our first approach is provide an interface allowing predefine rules that specify what happens if we see schema that matches known structures and which actions to perform. At run-time, the rules and the schemas of the source and target are given as input to generate the dataflow and prepended to the data pipeline.
>
> The goal is to achieve a fast, programmable data integration pipeline.

**Accuracy.** 

* Percentage of correct mappings. 
* Precision:
* Recall:
* F1 score:

**Performance.** 
* Latency: time it takes to finish a mint.
* Throughput: number of mints per second.

**Cost.** Token-efficiency. 



Llmint exposes the high-level modules with a declarative interface.

```python
import llmint
mint = llmint.new_mint()
```

> Difficult cases. 1. Same filed names but refer to different entities. 2. Range differences. 3. Data nested.

> TBD Example selection. Since it's unlikely that all examples are equally useful, llmint allows stateful matching with example selection to improve accuracy and reduce tokens

> TBD Completion model.

> TBD Deducting mapping from the values.

> TBD Semantic handshaking 

> TBD Support additional rules as part of examples

> TBD Small model async access

## FAQ

> Why not dump all data to LLM and let it generate results?

Structured queries over time series data can be done more efficiently (fast and less costs) with dataflow engines. 

> Data integration is hard. How does LLM help solve the problem?

Here are a few intuitions on why the approach works for some domains. In IoT, for example, here are a few characteristics. (i) Simple schemas. In IoT, for example, the data source generates continuous stream of data records. (ii) Large volume of data. (iii) Description of the data source.

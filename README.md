# llmint
Fast, adaptive, modular data integration toolchain powered by LLM.

Given data from a data provider (source) and a data consumer (target):
```yaml
source: { "status": "on", "brightness": 90 }
target: { "power": "active", "luminosity": 0.9 }
```
We want to generate dataflow operators that convert data from the source schema to the target schema, given information about the data source and the data consumer, with a process we refer to as *mint*. 

```shell
rename power := status | rename luminosity := brightness | switch power ("on" => power := "active" "off" => power := "inactive")
```



A mint operation consists of the following stages.

**S1: Discovery.** Identifying the data sources that are relevant to a data consumer based on the *intent* at the data consumer and the data source's *metadata* such as text description. This stage helps scope down the semantics of the desired schema and can be seen as a pre-filtering step. Data consumer can also use this step to select known data sources.

**S2: Extraction.** This stage extracts the schemas from the data source and consumer and represent them in a mint intermediate representation (MR). It allows the mint process to handle a diverse set of data sources (e.g., json files, data lakes, databases, API endpoints) while passing on a unified schema format to the next stages.

**S3: Identification.** Given the source and target MRs this stage (i) preprocesses them to generate normalized MRs which are invariant to field ordering, capitalization etc; (ii) decides whether the source-target schema pair has been seen before. If so, skip the following steps and return any cached correspondences or mappings.

**S4: Matching.** Find the correspondences between fields in the schemas. This step generates the correspondence between fields. Each correspondence contains a language-neutral transformation between the values and can be seen as a row of a match-action table. The process Decides whether the schemas are semantically equivalent and/or having semantically equivalent fields, depending on the pre-filtering policy.

**S5: Mapping.** Generates dataflow that coverts fields from source schema to the target schema, given the correspondences. The dataflow language can be specified by the user.

S1-S3 are referred to as the frontend which extracts source schema from desired data sources. S4-S5 are referred to as the backend.  The mapping dataflow can be installed on the data pipeline or used in a query.

## Design

Llmint focuses on three objectives: accuracy, performance, and cost.

> JIT data ingestion: A data processing pipeline typically ingests data from predefined data sources only. This limits the types of data it can ingest (i.e., a schema or a set of schemas), because the dataflow operators typically can perform over known fields. Instead, we want the data pipeline to be able to handle more data that are semantically equivalent but with different schemas. This means we want to dynamically adapt the pipeline (i.e., its ingestion component) based on the data source schema.
>
> Our first approach is provide an interface allowing predefine rules that specify what happens if we see schema that matches known structures and which actions to perform. At run-time, the rules and the schemas of the source and target are given as input to generate the dataflow and prepended to the data pipeline.
>
> 
>
> The goal is to achieve a fast, programmable data integration pipeline.



**Accuracy.** 

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
corr = mint.
```



Difficult cases. 1. Same filed names but refer to different entities. 2. Range differences. 3. Data nested.



## FAQ

> Why not dump all data to LLM and let it generate results?

Structured queries over time series data can be done more efficiently (fast and less costs) with dataflow engines. 

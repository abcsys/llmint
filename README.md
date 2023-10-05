# llmint
Fast, adaptive, modular data integration toolchain powered by LLM.

Given data from a data provider (source) and a data consumer (target):
```yaml
source: { "status": "on", "brightness": 90 }
target: { "power": "active", "luminosity": 0.9 }
```
We want to generate the dataflow operators that convert data from the source schema to the target schema. A mint process consists of the following stages.

S1. Discovery. Identifying the data sources that are relevant to a data consumer based on metadata such as text description of the data source and the intent at the data consumer.

S2. Normalization. This step preprocesses all schemas and generates a unique schema fingerprint which is invariant to field ordering, capitalization etc. Extracts the schema from the data.

S3. Identification. Decides (i) whether the schema has been seen before. If so, skip the following steps. (ii) Decides whether the schemas are semantically equivalent and/or having semantically equiavalent fields. 

S4. Matching. Find the correspondences between fields in the schemas. This step generates the correspondence between fields. Each correspondence contains a language-neutral transformation between the values and can be seen as a row of a match-action table.

S5. Mapping. Generates dataflow that coverts fields from source schema to the target schema, given the correspondances.

The generated dataflow can be installed on the dataflow engine.


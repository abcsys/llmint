
<a name="readme-top"></a>

<h1 align="center">LLMint's Command Module</h1>

<p align="center">
    Framework for generating structured mappings between well-formatted schemas, powered by OpenAI.
</p>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-module">About The Module</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
        <li><a href="#field-transformation-commands">Field Transformation Commands</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Module

This module is for the <span style="color:orange">mapping</span> stage of llmint. Given a well-formatted source and target schema from the previous extraction stage, this module will return a list of structured *mappings*. A mapping defines the transformation required to map between a field in the source schema and its corresponding field in the target schema. There may be multiple mappings required for a single pair of fields.

### Built With 
[![OpenAI][OpenAI.com]][OpenAI-url]

### Field Transformation Commands
* `doNothing`: no mapping is needed for a pair of fields
```yaml
{from: {source_field}, to: {target_field}, transformation: KEEP}
```
* `addOptional`: instead of mapping from a source field, generate an optional target field by directly adding it
```yaml
{from: None, to: {target_field}, transformation: ADD {target_field} TYPE {field_type}}
```
* `cast`: change the type of the source field
```yaml
{from: {source_field}, to: {target_field}, transformation: CAST {source_field} FROM {source_type} TO {target_type}}
```
* `delete`: delete the source field
```yaml
{from: {source_field}, to: None, transformation: DELETE {source_field}}
```
* `rename`: rename the source field
```yaml
{from: {source_field}, to: {target_field}, transformation: RENAME {source_field} TO {target_field}}
```
* `setDefault`: set the default of a target field
```yaml
{from: {source_field}, to: {target_field}, transformation: SET_DEFAULT {target_field} TO {default_value}}
```

### Value Transformation Commands
* `applyFunc`:
* `map`:
* `scale`:
* `shift`:

### Extended Commands
* `combine`:
* `split`:
* `missing`:
* `complexConversion`:
* `incompatible`:
* `sendMessage`:

Here's why:
* Your time should be focused on creating something amazing. A project that solves a problem and helps others
* You shouldn't be doing the same tasks over and over like creating a README from scratch
* You should implement DRY principles to the rest of your life :smile:

Of course, no one template will serve all projects since your needs may be different. So I'll be adding more in the near future. You may also suggest changes by forking this repo and creating a pull request or opening an issue. Thanks to all the people have contributed to expanding this template!

Use the `BLANK_README.md` to get started.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
[OpenAI.com]: https://img.shields.io/badge/OPENAI_GPT4-Function_Calling-000000?style=for-the-badge&logo=openai&logoColor=white
[OpenAI-url]: https://platform.openai.com/docs/guides/function-calling
## Example 4: Auto-Select Model

When you're not sure which model is available:

```
User: "Can you describe this image using whatever model is available?"
Claude: "I'll analyze the image using the best available model."

[Claude uses describe_image_auto tool]
```

## PDF Extraction Examples

### Example 5: Extract PDF Content (Default)

```
User: "Can you extract and analyze the content from this PDF?"
Claude: "I'll extract the content from your PDF document."

[Claude uses extract_pdf_content tool with default settings]
```

### Example 6: Extract PDF with Text Focus

```
User: "Extract the text and images separately from this PDF"
Claude: "I'll extract the text and images separately from your PDF."

[Claude uses extract_pdf_content tool with method="text_and_images"]
```

### Example 7: Extract PDF with Visual Analysis

```
User: "Analyze this PDF focusing on the visual layout and design"
Claude: "I'll analyze your PDF with focus on visual elements and layout."

[Claude uses extract_pdf_content tool with method="page_as_image"]
```

### Example 8: Comprehensive PDF Analysis

```
User: "Give me a comprehensive analysis of this PDF including both text and visual elements"
Claude: "I'll perform a comprehensive analysis using the hybrid extraction method."

[Claude uses extract_pdf_content tool with method="hybrid"]
```

## Tips for MCP Tool Usage

1. **File Paths**: When using MCP tools, ensure file paths are accessible from where the API server is running
2. **API Keys**: Configure API keys in environment variables for security
3. **Error Handling**: MCP tools include helpful error messages and suggestions
4. **Performance**:
   - `page_as_image` is best for visual-heavy PDFs
   - `text_and_images` is fastest for text-heavy PDFs
   - `hybrid` provides the most comprehensive results but takes longer

## Common Issues and Solutions

### Issue: "API key required"
**Solution**: Set the OPENAI_API_KEY environment variable or pass it in the request

### Issue: "Ollama connection refused"
**Solution**: Ensure Ollama is running locally on port 11434

### Issue: "PDF extraction failed"
**Solution**: Try a different extraction method - some PDFs work better with specific methods

### Issue: "No description generated"
**Solution**: Check that the image file is valid and accessible

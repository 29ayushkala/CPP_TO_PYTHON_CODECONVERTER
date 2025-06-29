let pyodide = null;

async function initPyodide() {
    if (!pyodide) {
        document.getElementById('loading').style.display = 'block';
        try {
            pyodide = await loadPyodide();
            await pyodide.loadPackage('micropip');
            await pyodide.runPythonAsync(`
import micropip
await micropip.install('ply')
            `);
            const response = await fetch('transpiler.py?t=' + new Date().getTime());
            if (!response.ok) {
                throw new Error(`Failed to fetch transpiler.py: ${response.statusText}`);
            }
            const transpilerCode = await response.text();
            console.log('Loaded transpiler.py (first 500 chars):', transpilerCode.substring(0, 500));
            // Write transpiler.py to Pyodide's virtual file system
            pyodide.FS.writeFile('/transpiler.py', transpilerCode);
            // Import the transpiler module
            await pyodide.runPythonAsync(`
import sys
sys.path.append('/')
import transpiler
            `);
        } catch (err) {
            document.getElementById('error').textContent = `Initialization Error: ${err.message}\nDetails: ${err.stack || 'No stack trace available'}`;
            throw err;
        } finally {
            document.getElementById('loading').style.display = 'none';
        }
    }
}

async function convertCode() {
    const cppCode = document.getElementById('cpp-code').value;
    const pythonOutput = document.getElementById('python-code');
    const errorDiv = document.getElementById('error');
    const loadingDiv = document.getElementById('loading');

    pythonOutput.value = '';
    errorDiv.textContent = '';
    loadingDiv.style.display = 'block';

    try {
        await initPyodide();
        const escapedCppCode = cppCode.replace(/"""/g, '\\"\\"\\"');
        const result = await pyodide.runPythonAsync(`from transpiler import transpile\ntranspile("""${escapedCppCode}""")`);
        pythonOutput.value = result;
    } catch (err) {
        errorDiv.textContent = `Error: ${err.message}\nDetails: ${err.stack || 'No stack trace available'}`;
    } finally {
        loadingDiv.style.display = 'none';
    }
}

import React, { useState } from "react";
import AceEditor from "react-ace";

import "ace-builds/src-noconflict/mode-javascript";
import "ace-builds/src-noconflict/theme-github";
import "ace-builds/src-noconflict/theme-monokai";
import "ace-builds/src-noconflict/theme-terminal";

function CodeEditor({ handleCodeChange }) {
  return (
    <>
      <AceEditor
        mode="javascript"
        theme="terminal"
        name="123"
        fontSize={18}
        width="70vw"
        height="97vh"
        onChange={handleCodeChange}
        editorProps={{ $blockScrolling: true }}
      />
    </>
  );
}

export default CodeEditor;

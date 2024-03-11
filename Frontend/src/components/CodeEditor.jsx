import React, { useState } from "react";
import AceEditor from "react-ace";

import "ace-builds/src-noconflict/mode-javascript";
import "ace-builds/src-noconflict/theme-github";
import "ace-builds/src-noconflict/theme-monokai";

function CodeEditor({ handleCodeChange }) {
  return (
    <>
      <AceEditor
        mode="javascript"
        theme="monokai"
        name="123"
        fontSize={18}
        width="auto"
        // height="985px"
        onChange={handleCodeChange}
        editorProps={{ $blockScrolling: true }}
      />
    </>
  );
}

export default CodeEditor;

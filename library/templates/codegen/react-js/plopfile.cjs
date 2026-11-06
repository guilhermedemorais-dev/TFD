const path = require('node:path');

module.exports = function register(plop) {
  plop.setGenerator('react-component', {
    description: 'Generate a named JavaScript/JSX component in the selected project',
    prompts: [{ type: 'input', name: 'name', message: 'Component name (PascalCase)' }],
    actions(data) {
      if (!/^[A-Z][A-Za-z0-9]*$/.test(data.name || '')) {
        throw new Error('Use a PascalCase identifier without path separators.');
      }
      return [{
        type: 'add',
        path: path.join(process.cwd(), 'src/components/{{name}}/{{name}}.jsx'),
        templateFile: path.join(__dirname, 'templates/component.jsx.hbs'),
        force: false,
        abortOnFail: true,
      }];
    },
  });
};

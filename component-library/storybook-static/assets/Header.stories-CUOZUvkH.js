import{j as r}from"./jsx-runtime-D_zvdyIk.js";const d=({title:u,subtitle:n,align:m="left"})=>r.jsxs("div",{style:{textAlign:m},children:[r.jsx("h1",{children:u}),n?r.jsx("p",{children:n}):null]});d.__docgenInfo={description:"",methods:[],displayName:"Header",props:{title:{required:!0,tsType:{name:"string"},description:""},subtitle:{required:!1,tsType:{name:"string"},description:""},align:{required:!1,tsType:{name:"union",raw:"'left' | 'center' | 'right'",elements:[{name:"literal",value:"'left'"},{name:"literal",value:"'center'"},{name:"literal",value:"'right'"}]},description:"",defaultValue:{value:"'left'",computed:!1}}}};const g={title:"Content/Header",component:d},e={args:{title:"Welcome",subtitle:"Start here",align:"left"}},t={args:{title:"Centered",subtitle:"Subtitle",align:"center"}};var a,s,l;e.parameters={...e.parameters,docs:{...(a=e.parameters)==null?void 0:a.docs,source:{originalSource:`{
  args: {
    title: 'Welcome',
    subtitle: 'Start here',
    align: 'left'
  }
}`,...(l=(s=e.parameters)==null?void 0:s.docs)==null?void 0:l.source}}};var i,o,c;t.parameters={...t.parameters,docs:{...(i=t.parameters)==null?void 0:i.docs,source:{originalSource:`{
  args: {
    title: 'Centered',
    subtitle: 'Subtitle',
    align: 'center'
  }
}`,...(c=(o=t.parameters)==null?void 0:o.docs)==null?void 0:c.source}}};const f=["Default","Centered"];export{t as Centered,e as Default,f as __namedExportsOrder,g as default};

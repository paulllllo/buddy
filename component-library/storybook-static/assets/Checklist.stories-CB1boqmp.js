import{j as r}from"./jsx-runtime-D_zvdyIk.js";import{r as o}from"./index-CY-HDqYb.js";const p=({items:t,onChange:s})=>{const[l,i]=o.useState(t);o.useEffect(()=>{i(t)},[t]);const b=e=>{const d=l.map(a=>a.id===e?{...a,checked:!a.checked}:a);i(d),s==null||s(d)};return r.jsx("ul",{style:{listStyle:"none",padding:0,margin:0},children:l.map(e=>r.jsx("li",{style:{marginBottom:8},children:r.jsxs("label",{children:[r.jsx("input",{type:"checkbox",checked:!!e.checked,disabled:e.disabled,onChange:()=>b(e.id)}),r.jsx("span",{style:{marginLeft:8},children:e.label})]})},e.id))})};p.__docgenInfo={description:"",methods:[],displayName:"Checklist",props:{items:{required:!0,tsType:{name:"Array",elements:[{name:"signature",type:"object",raw:`{\r
	id: string;\r
	label: string;\r
	checked?: boolean;\r
	disabled?: boolean;\r
}`,signature:{properties:[{key:"id",value:{name:"string",required:!0}},{key:"label",value:{name:"string",required:!0}},{key:"checked",value:{name:"boolean",required:!1}},{key:"disabled",value:{name:"boolean",required:!1}}]}}],raw:"ChecklistItem[]"},description:""},onChange:{required:!1,tsType:{name:"signature",type:"function",raw:"(items: ChecklistItem[]) => void",signature:{arguments:[{type:{name:"Array",elements:[{name:"signature",type:"object",raw:`{\r
	id: string;\r
	label: string;\r
	checked?: boolean;\r
	disabled?: boolean;\r
}`,signature:{properties:[{key:"id",value:{name:"string",required:!0}},{key:"label",value:{name:"string",required:!0}},{key:"checked",value:{name:"boolean",required:!1}},{key:"disabled",value:{name:"boolean",required:!1}}]}}],raw:"ChecklistItem[]"},name:"items"}],return:{name:"void"}}},description:""}}};const h={title:"Form/Checklist",component:p},n={args:{items:[{id:"1",label:"Read handbook"},{id:"2",label:"Sign NDA",checked:!0}]}};var c,m,u;n.parameters={...n.parameters,docs:{...(c=n.parameters)==null?void 0:c.docs,source:{originalSource:`{
  args: {
    items: [{
      id: '1',
      label: 'Read handbook'
    }, {
      id: '2',
      label: 'Sign NDA',
      checked: true
    }]
  }
}`,...(u=(m=n.parameters)==null?void 0:m.docs)==null?void 0:u.source}}};const y=["Default"];export{n as Default,y as __namedExportsOrder,h as default};

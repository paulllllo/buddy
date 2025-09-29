import{j as t}from"./jsx-runtime-D_zvdyIk.js";const g=({type:v,src:s,alt:a,controls:y=!0,width:n="100%",height:o,style:i})=>v==="image"?t.jsx("img",{src:s,alt:a??"",style:{width:n,height:o,...i}}):t.jsx("video",{src:s,controls:y,style:{width:n,height:o,...i},children:a?t.jsx("track",{kind:"captions",label:a}):null});g.__docgenInfo={description:"",methods:[],displayName:"Media",props:{type:{required:!0,tsType:{name:"union",raw:"'image' | 'video'",elements:[{name:"literal",value:"'image'"},{name:"literal",value:"'video'"}]},description:""},src:{required:!0,tsType:{name:"string"},description:""},alt:{required:!1,tsType:{name:"string"},description:""},controls:{required:!1,tsType:{name:"boolean"},description:"",defaultValue:{value:"true",computed:!1}},width:{required:!1,tsType:{name:"union",raw:"number | string",elements:[{name:"number"},{name:"string"}]},description:"",defaultValue:{value:"'100%'",computed:!1}},height:{required:!1,tsType:{name:"union",raw:"number | string",elements:[{name:"number"},{name:"string"}]},description:""},style:{required:!1,tsType:{name:"ReactCSSProperties",raw:"React.CSSProperties"},description:""}}};const f={title:"Content/Media",component:g},e={args:{type:"image",src:"https://via.placeholder.com/400x200",alt:"Placeholder"}},r={args:{type:"video",src:"https://www.w3schools.com/html/mov_bbb.mp4",alt:"Sample video"}};var m,l,p;e.parameters={...e.parameters,docs:{...(m=e.parameters)==null?void 0:m.docs,source:{originalSource:`{
  args: {
    type: 'image',
    src: 'https://via.placeholder.com/400x200',
    alt: 'Placeholder'
  }
}`,...(p=(l=e.parameters)==null?void 0:l.docs)==null?void 0:p.source}}};var c,d,u;r.parameters={...r.parameters,docs:{...(c=r.parameters)==null?void 0:c.docs,source:{originalSource:`{
  args: {
    type: 'video',
    src: 'https://www.w3schools.com/html/mov_bbb.mp4',
    alt: 'Sample video'
  }
}`,...(u=(d=r.parameters)==null?void 0:d.docs)==null?void 0:u.source}}};const b=["Image","Video"];export{e as Image,r as Video,b as __namedExportsOrder,f as default};

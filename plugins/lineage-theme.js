const customTheme = document.createElement('dom-module');
	
/*customTheme.innerHTML = `
/<template>
  <style>
    :root {
      --header-background-color: #167c80;
      --header-text-color: #fff;
      --header-title-content: "LineageOS Gerrit";
      --header-icon: url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADEAAAAYCAYAAABTPxXiAAAACXBIWXMAAAsSAAALEgHS3X78AAADVUlEQVRYw+2XMWxbVRSGv0Ik34jKvh7aOlIcOwMiaSPVRkWx3wABFsdLmyyxWFoJJUUgJQMMSDRKJWcrSBQEAioqjADZA8Fd6nQgNAMOVaPYURM5iMGOksHu9GxleB4qMcC79eM9t5RWioGc6ene8+65//nPf++5h45euHgRmOPfa8tP8R+wAxCdYl1PekGPEExpERLhEL3So8YbRpNcaYt0oUi+XOlcEIlwiGQ8hlu4bHNu4WIifJKJ8EmurNziwvXFzgORCIe4PH7alnXThnp8nI9G6JUeJqPDuIVgeiHbOSCGenwKwGa1xtlv0+zousUnX66QWSuSjMcUIzu6zqWlm50h7GQ8phgY+/IrGwDT6obB9EKWxdKvAExFI3iE2H8QfinRggEAZq8vUjcMVV6/vfcuteQcteQc838CBZQe3MLF6ODA/oMY6vGpb1MDfim5PH7aIvDJ6DBTWgSAHV1XbOw7CI8QahP5yvZ9kT8fcvRv3fBGtfoHYK+0JOKJCns+HmMiHFLZzFe2mf4+i6dbkAiH0PqDnPAde+wsnvAd48c3z7Or1/m5XCFX2iJX2mob30lvjiBSryWIDT5nGdOCAVbfnmm7GVMXAOm1Iu+8/JLNJ7PWcuT6rNnvlR51ajWMpu2u0YIBlt56g1MffKh017achnp8CkCmsM7Y1RSzuRsWn4bRJFNY59x3GV799HPLXWHW/MzCNRpGU81dWbll0YwZY2bhGmNXU7z/0zKb1ZoSvFN8t3ApXT2QCbNud/W6uozy5Qp9UjIZHWazWuOVTz6z3gGVbbRggGQ8Rq60Rd0wSBeKpAtF/FLaSmC+5Ug2/fPlCpeWbjIfjzEZHW4bX+sPPr6w/0qlebSamfrh9XP4pVRzrQA8QvDR+BnFwhcrv9jWc1r/Yfb0My+OjAAj90vF4OwLp3ALQZ/XS90wGD0+oGo8U1i3NXB39/bY1euMDg5w9PBhprSI+tfvlfi9ktHjA3w8fgatP6DWmXXon/5B/O1DTi87J2Gb9DsJ6+80gK32sAbwEeMv25gAyN7ZQHZ38+yRI7i6ulTdJ1LfcHdvr23wjWqVr2+v0rx3jz6vF3dLS9EwmmTvbDKbu0Hq9uoDQT5ifGcmDt7YB8/T/zGI3wHyQoXZnoBIowAAAABJRU5ErkJggg==');
      --header-icon-size: 0em;
    }
  </style>
</template
`;
*/
customTheme.register('lineage-review-theme');

Gerrit.install(plugin => {
	const style = document.createElement('style');
	style.innerHTML = `
		:root {
		      --header-background-color: #167c80;
		      --header-text-color: #fff;
		      --header-title-content: "LineageOS Gerrit";
		      --header-icon: url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADEAAAAYCAYAAABTPxXiAAAACXBIWXMAAAsSAAALEgHS3X78AAADVUlEQVRYw+2XMWxbVRSGv0Ik34jKvh7aOlIcOwMiaSPVRkWx3wABFsdLmyyxWFoJJUUgJQMMSDRKJWcrSBQEAioqjADZA8Fd6nQgNAMOVaPYURM5iMGOksHu9GxleB4qMcC79eM9t5RWioGc6ene8+65//nPf++5h45euHgRmOPfa8tP8R+wAxCdYl1PekGPEExpERLhEL3So8YbRpNcaYt0oUi+XOlcEIlwiGQ8hlu4bHNu4WIifJKJ8EmurNziwvXFzgORCIe4PH7alnXThnp8nI9G6JUeJqPDuIVgeiHbOSCGenwKwGa1xtlv0+zousUnX66QWSuSjMcUIzu6zqWlm50h7GQ8phgY+/IrGwDT6obB9EKWxdKvAExFI3iE2H8QfinRggEAZq8vUjcMVV6/vfcuteQcteQc838CBZQe3MLF6ODA/oMY6vGpb1MDfim5PH7aIvDJ6DBTWgSAHV1XbOw7CI8QahP5yvZ9kT8fcvRv3fBGtfoHYK+0JOKJCns+HmMiHFLZzFe2mf4+i6dbkAiH0PqDnPAde+wsnvAd48c3z7Or1/m5XCFX2iJX2mob30lvjiBSryWIDT5nGdOCAVbfnmm7GVMXAOm1Iu+8/JLNJ7PWcuT6rNnvlR51ajWMpu2u0YIBlt56g1MffKh017achnp8CkCmsM7Y1RSzuRsWn4bRJFNY59x3GV799HPLXWHW/MzCNRpGU81dWbll0YwZY2bhGmNXU7z/0zKb1ZoSvFN8t3ApXT2QCbNud/W6uozy5Qp9UjIZHWazWuOVTz6z3gGVbbRggGQ8Rq60Rd0wSBeKpAtF/FLaSmC+5Ug2/fPlCpeWbjIfjzEZHW4bX+sPPr6w/0qlebSamfrh9XP4pVRzrQA8QvDR+BnFwhcrv9jWc1r/Yfb0My+OjAAj90vF4OwLp3ALQZ/XS90wGD0+oGo8U1i3NXB39/bY1euMDg5w9PBhprSI+tfvlfi9ktHjA3w8fgatP6DWmXXon/5B/O1DTi87J2Gb9DsJ6+80gK32sAbwEeMv25gAyN7ZQHZ38+yRI7i6ulTdJ1LfcHdvr23wjWqVr2+v0rx3jz6vF3dLS9EwmmTvbDKbu0Hq9uoDQT5ifGcmDt7YB8/T/zGI3wHyQoXZnoBIowAAAABJRU5ErkJggg==');
		      --header-icon-size: 0em;
	      }

	`
	document.head.appendChild(style)
	//plugin.registerStyleModule('app-theme', 'lineage-review-theme');
});
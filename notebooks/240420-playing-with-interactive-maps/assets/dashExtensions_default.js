window.dashExtensions = Object.assign({}, window.dashExtensions, {
    default: {
        function0: function(feature, context) {
            // get props from hideout
            const {
                min,
                max,
                classes,
                colorscale,
                style,
                colorProp
            } = context.hideout;
            // get value the determines the color
            const value = feature.properties[colorProp];
            // chroma lib to construct colorscale
            const csc = chroma.scale(colorscale).domain([min, max]);
            for (let i = 0; i < classes.length; ++i) {
                if (value > classes[i]) {
                    // set color based on color prop
                    style.fillColor = csc(feature.properties[colorProp]);
                }
            }
            return style;
        }
    }
});
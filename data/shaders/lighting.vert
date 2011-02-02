
attribute vec3 position;
attribute vec3 color;
attribute vec3 normal;

void main()
{
    vec3 LightPosition = vec3(0.2670, 0.267 * 3.0, 0.2673 * 2.0);

    vec3 tnorm = normalize(gl_NormalMatrix * normal);
    float costheta = dot(tnorm, LightPosition);
    float a = 0.85 + 0.15 * costheta;

    gl_FrontColor = vec4(color.rgb * a, 1.0);
    gl_Position = gl_ModelViewProjectionMatrix * vec4(position, 1.0);
    gl_TexCoord[0] = gl_MultiTexCoord0;
}


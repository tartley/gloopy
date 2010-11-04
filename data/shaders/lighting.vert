
void main()
{
    vec3 LightPosition = vec3(0.2670, 0.267 * 3.0, 0.2673 * 2.0);

    vec3 tnorm = normalize(gl_NormalMatrix * gl_Normal);
    float costheta = dot(tnorm, LightPosition);
    float a = 0.85 + 0.15 * costheta;

    gl_FrontColor = vec4(gl_Color.rgb * a, gl_Color.a);
    gl_Position = ftransform();
    gl_TexCoord[0] = gl_MultiTexCoord0;
}


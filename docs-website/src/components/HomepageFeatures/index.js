import clsx from 'clsx';
import Heading from '@theme/Heading';
import styles from './styles.module.css';

const FeatureList = [
  {
    title: 'Exact API Reflection',
    // Svg: require('@site/static/img/undraw_docusaurus_mountain.svg').default,
    description: (
      <>
        aiorocket2 mirrors the xRocket API almost exactly — 
        all methods, parameters, models, and enums are faithfully 
        preserved. No surprises, everything you know from the API
        works the same way.
      </>
    ),
  },
  {
    title: 'Fully Asynchronous',
    // Svg: require('@site/static/img/undraw_docusaurus_tree.svg').default,
    description: (
      <>
        Built with asyncio from the ground up — every request
        is non-blocking, making your projects fast, smooth, and
        ready for modern Python async workflows.
      </>
    ),
  },
  {
    title: 'Open for the Community',
    // Svg: require('@site/static/img/undraw_docusaurus_react.svg').default,
    description: (
      <>
        aiorocket is open source and welcomes contributions.
        Report issues, submit pull requests, suggest improvements
        — your input shapes the library.
      </>
    ),
  },
];

function Feature({title, description}) {
  return (
    <div className={clsx('col col--4')}>
      <div className="text--center">
        {/* <Svg className={styles.featureSvg} role="img" /> */}
      </div>
      <div className="text--center padding-horiz--md">
        <Heading as="h3">{title}</Heading>
        <p>{description}</p>
      </div>
    </div>
  );
}

export default function HomepageFeatures() {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}
